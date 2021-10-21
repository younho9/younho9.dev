---
hero: ./images/2021-10-21-how-to-iterate-object-more-safely.jpeg
slug: 'how-to-iterate-object-more-safely'
title: '타입스크립트에서 객체를 "더 안전하게" 순회하는 방법 (feat: 무공변성)'
date: 2021-10-21
tags: ['TypeScript', 'Object']
author: younho9
excerpt: 구조적 타입 시스템에서 무공변 타입을 사용해 객체를 더 안전하게 순회해보자.
---

> Photo By [@Chris Fowler](https://unsplash.com/photos/m-U6Y8K3i5k?utm_source=unsplash&utm_campaign=wallpapers-macos&utm_medium=referral&content=view-photo-on-unsplash)

## TL;DR

- 타입스크립트는 **구조적 타입 시스템**을 따르기 때문에 **타입이 '열려' 있다.**
- 타입스크립트에서 **'봉인된' 또는 '정확한'** 타입을 만드는 방법에는 **명목적 타입과 무공변적 타입**이 있다.
- **명목적 타입 시스템**은 **구조가 같더라도 이름이 다르면 다른 타입**으로 구분하는 시스템이다.
- 무공변적 타입은 **정확히 동일한, 타입을 요구**하는 타입 호환 방식이다.
- 명목적 타입과 무공변적 타입을 통해 **객체를 보다 안전하게 순회하면서, 구체적인 타입**을 얻을 수 있다.
- 하지만 트릭적인 요소가 포함되므로, **타입스크립트의 구조적 타입 시스템을 따르는 것**이 보다 권장된다.

## 구조적 타입 시스템과 `Object.keys`

타입스크립트는 [구조적 타입 시스템(Structural Type System)](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html#structural-type-system)을 따른다.

이러한 특성으로 인해 객체의 키를 가지고 객체에 접근할 때 한 가지 문제를 겪게 된다.

```typescript
type Person = {
  name: string;
  age: number;
  id: number;
};

declare const me: Person;

Object.keys(me).forEach((key) => {
  // No index signature with a parameter of type 'string' was found on type 'Person'.(7053)
  console.log(me[key]);
});
```

에러의 원인을 찾다 보면 `Object.keys`의 반환 타입이 `string[]` 이기 때문에 발생한 것을 알 수 있다.

```typescript
interface ObjectConstructor {
  //...
  keys(o: object): string[];
  keys(o: {}): string[];
}
```

`Person` 타입의 객체에 접근할 수 있는 실제 키는 `name | age | id` 타입인데, `Object.keys`로 얻은 key는 그에 상위 집합인 `string` 타입이기 때문에 접근할 수 없는 것이다.

그러면 이 메서드의 시그니쳐를 다음과 같이 변경할 순 없을까?

```typescript
interface ObjectConstructor {
  // ...
  keys<O extends object>(o: O): (keyof O)[];
}
```

이렇게 타이핑 했을 때의 문제는 이 [이슈 코멘트](https://github.com/microsoft/TypeScript/pull/12253#issuecomment-263132208)에서 볼 수 있다.

요약하면 **객체는 런타임에 더 많은 속성을 가질 수 있기 때문에**, `(keyof O)[]`은 좁은 타입이고, `string[]` 타입이 정확한 타입이라는 것이다.

이러한 상황을 [재현한 예제](https://twitter.com/phry/status/1348982969575346183)는 다음과 같다.

```typescript
interface AB {
  a: string;
  b: string;
}

function someFunction(arg: AB) {
  // 만약 Object.keys가 string[]이 아니라 (keyof AB)[] 타입을 리턴한다면 ...
  return Object.keys(arg) as (keyof AB)[];
}

const myArgument = {
  a: 'some',
  b: 'thing',
  c: 'unexpected',
};

// myArgument는 매개변수 타입 AB에 호환된다.
// 따라서, 실제로는 ('a' | 'b' | 'c')[]이 리턴될 것이고, (keyof AB)[] 타입은 오류라는 것을 알 수 있다.
someFunction(myArgument);
```

아래의 두 글은 구조적 타입 시스템을 따르는 타입스크립트에서 객체를 순회하는 방법을 소개한다.

- https://fettblog.eu/typescript-better-object-keys/
- https://effectivetypescript.com/2020/05/26/iterate-objects/

두 글에서는 `Object.entries` 를 사용하여 객체를 순회하거나, **객체에 다른 속성이 포함되지 않을 것을 확신할 수 있는 경우**에 `(keyof O)[]`로 캐스팅하여 사용할 것을 권한다.

하지만 **"캐스팅을 사용하지 않고, 객체의 키 타입을 구체적으로 얻을 수 있는 방법은 없을까?"** 고민하게 되었고, **무공변적(Invariant) 타입**을 사용하는 방법을 알게 되었다.

이 글에서는 무공변적 타입을 사용해 객체의 키 타입을 보다 구체적으로 얻는 방법에 대해 알게 된 내용을 다룬다.

## 무공변성이란?

먼저 무공변성이란 무엇인지 알아보자.

타입 시스템이 가질 수 있는 타입 호환성 또는 유형 변환 방식에는 공변성(Covariance), 반공변성(Contravariance), 무공변성(Invariance), 이변성(Bivariance)이 있다.

- https://flow.org/en/docs/lang/variance/

이 중, 무공변성은, 원본 타입의 슈퍼 타입이나 서브 타입도 호환하지 않는 **'봉인된(sealed)' 또는 '정확한(precise)'** 타입 호환성이다.

> 런타임에서 [`Object.seal`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/seal)로 만들어진 객체와 유사하다고 볼 수 있다.

```typescript
interface SuperType {
  foo: number;
}

interface BaseType extends SuperType {
  bar: string;
}

interface SubType extends BaseType {
  baz: boolean;
}

declare let superTypeValue: SuperType;
declare let baseTypeValue: BaseType;
declare let subTypeValue: SubType;

// 공변 (타입스크립트에서 변수는 공변이다.)
baseTypeValue = superTypeValue; // 에러!
baseTypeValue = subTypeValue; // 허용

// 반공변 (타입스크립트에서 함수의 매개변수는 반공변이다.)
baseTypeValue = superTypeValue; // 허용
baseTypeValue = subTypeValue; // 에러!

// 무공변
baseTypeValue = superTypeValue; // 에러!
baseTypeValue = subTypeValue; // 에러!

// 이변
baseTypeValue = superTypeValue; // 허용
baseTypeValue = subTypeValue; // 허용
```

### 타입스크립트의 유형 호환 규칙

타입스크립트는 크게 두 가지 유형 호환 규칙을 따른다.

1. [타입스크립트에서 변수는 공변](https://www.typescriptlang.org/ko/docs/handbook/type-compatibility.html#%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0-starting-out)한다.
2. [타입스크립트에서 두 함수의 타입을 비교할 때, 함수의 매개변수는 반공변성](https://www.typescriptlang.org/ko/docs/handbook/type-compatibility.html#%ED%95%A8%EC%88%98-%EB%A7%A4%EA%B0%9C%EB%B3%80%EC%88%98%EC%9D%98-bivariance-function-parameter-bivariance)을 가진다. (`--strictFunctionTypes` 옵션을 사용하는 경우)

따라서, 타입스크립트에서는 1번 규칙에 따라 **원본 타입을 만족한다면 추가적인 속성을 가지고 있어도 허용**하므로, 런타임에 객체에 더 많은 키가 존재할 수 있는 것이다.

그래서 타입스크립트에서도 "**정확한 타입**을 강제한다면, 객체의 키 타입을 구체적으로 알 수 있지 않을까?"하고 생각했고, 이를 만들 수 있는 방법을 찾기 시작했다.

## 명목적 타입 시스템

정확한 타입을 강제하는 방법 중 하나는 [명목적 타입(Nominal Type)](https://basarat.gitbook.io/typescript/main-1/nominaltyping) 또는 [불투명 타입(Opaque Type)](https://codemix.com/opaque-types-in-javascript/)으로 불리는 타입을 만들어서 사용하는 것이다.

명목적 타입은 두 변수의 **구조가 같더라도 유형의 이름이 다르면 다른 타입**으로 구분하는 시스템이다.

명목적 타입을 만드는 방법은 아래와 같이 **타입을 구분할 토큰을 `unique symbol` 프로퍼티로 가지는 `Tagged` 타입과 Intersect하는 것**이다.

```typescript
declare const tag: unique symbol;

declare type Tagged<Token> = {
  readonly [tag]: Token;
};

export type Opaque<Type, Token = unknown> = Type & Tagged<Token>;
```

> Opaque 타입에 대한 더 자세한 설명은 [여기](https://blog.beraliv.dev/2021-05-07-opaque-type-in-typescript/#choose-the-solution)를 참고

이 명목적 타입을 사용하면 무공변성과 유사하게 동작하도록 만들 수 있다.

```typescript
interface SuperType {
  foo: number;
}

interface BaseType extends SuperType {
  bar: string;
}

interface SubType extends BaseType {
  baz: boolean;
}

declare let superTypeValue: Opaque<SuperType, 'SuperType'>;
declare let baseTypeValue: Opaque<BaseType, 'BaseType'>;
declare let subTypeValue: Opaque<SubType, 'SubType'>;

baseTypeValue = superTypeValue; // 에러!
baseTypeValue = subTypeValue; // 에러!

// 명목적 타입으로 만들어주는 브랜드 함수
function createBaseType(base: BaseType): Opaque<BaseType, 'BaseType'> {
  return base as Opaque<BaseType, 'BaseType'>;
}

baseTypeValue = createBaseType({foo: 123, bar: 'hello'});
```

그러면 이제 명목적으로 타이핑된 객체의 경우에는, **'봉인된', '정확한'** 타입이므로 `Object.keys`의 리턴 타입을 구체적으로 만들 수 있을 것이다.

```typescript
interface AB {
  a: string;
  b: string;
}

type NominalAB = Opaque<AB, 'AB'>;

// 명목적 타입으로 만들어주는 브랜드 함수
function createAB(ab: AB): NominalAB {
  return ab as NominalAB;
}

function getKeysOfAB(arg: NominalAB): (keyof AB)[] {
  return Object.keys(arg) as (keyof AB)[];
}

const invalidArgument = {
  a: 'some',
  b: 'thing',
  c: 'unexpected',
};

const validArgument = createAB({
  a: 'some',
  b: 'thing',
});

let keys: (keyof AB)[];

keys = getKeysOfAB(invalidArgument); // 에러!
keys = getKeysOfAB(validArgument);
```

물론 브랜드 함수 자체는 구조적 타입으로 작성되기 때문에 런타임 에러의 가능성이 없는 것은 아니다.

하지만 브랜드 함수의 특성상 개발자가 주의를 기울이게 하는 효과가 있기 때문에, 보다 안전한 방법이라고 할 수 있다.

```typescript
function createAB(ab: AB): NominalAB {
  return ab as NominalAB;
}

interface ABC extends AB {
  c: boolean;
}

declare const abc: ABC;

createAB(abc); // Okay... But...
```

하지만 단지 객체의 키를에 대한 타입을 얻기 위해서 모든 타입을 명목적으로 작성해야 한다면 각각의 이름과 브랜드 함수를 모두 만들어 주어야 한다.

명목적 타입이 아닌 무공변적 타입을 타입스크립트에서 만드는 방법은 없을까?

## 무공변적 타입 만들기

### 첫 번째 접근

무공변적 타입을 만들기 위한 첫 번째 접근은 위의 명목적 타입을 만드는 방법에서 힌트를 얻었다.

`Opaque` 타입이 **타입을 구분할 토큰을 프로퍼티로 가지는 `Tagged` 타입과 Intersect하는 것**이라면,

무공변적 타입은 "**객체 타입의 키들(`keyof O`)을 구분할 토큰**으로 사용하면 되지 않을까?" 생각했다.

```typescript
declare const tag: unique symbol;

declare type Tagged<Token> = {
  readonly [tag]: Token;
};

export type Opaque<Type, Token = unknown> = Type & Tagged<Token>;

export type InvariantOf<O extends object> = Opaque<O, keyof O>;
```

이렇게 만든 무공변적 타입은 객체 타입이라는 제약하에 효과가 있었다.

```typescript
interface SuperType {
  foo: number;
}

interface BaseType extends SuperType {
  bar: string;
}

interface SubType extends BaseType {
  baz: boolean;
}

declare let superTypeValue: InvariantOf<SuperType>;
declare let baseTypeValue: InvariantOf<BaseType>;
declare let subTypeValue: InvariantOf<SubType>;

baseTypeValue = superTypeValue; // 에러!
baseTypeValue = subTypeValue; // 에러!

// 무공변 타입으로 만들어주는 함수
function invariantOf<O extends object>(base: O): InvariantOf<O> {
  return base as InvariantOf<O>;
}

baseTypeValue = invariantOf({foo: 123, bar: 'hello'});
```

하지만 무공변성은 객체 타입 뿐만 아니라, `number` 타입과 리터럴 `1` 타입의 관계나 `number | string` 타입과 `string` 타입의 관계에서도 적용되어야 하므로 불완전했다.

## 두 번째 접근

<!-- prettier-ignore-start -->
두 번째 방법은 [이 글](https://overcurried.com/%EC%9C%A0%EB%A0%B9%20%ED%83%80%EC%9E%85/)을 통해 알게 되었는데, 위에 서술한 [타입스크립트 유형 호환 규칙](#타입스크립트의-유형-호환-규칙)에 따라 **매개변수와 리턴 타입으로 특정 타입을 동시에 가지는 함수의 타입**을 사용함으로 무공변적 타입을 만들 수 있다.
<!-- prettier-ignore-end -->

```typescript
declare const tag: unique symbol;

declare type InvariantProperty<Type> = (arg: Type) => Type;

declare type InvariantSignature<Type> = {
  readonly [tag]: InvariantProperty<Type>;
};

export type InvariantOf<Type> = Type & InvariantSignature<Type>;
```

즉, `InvariantPropety<Type>`은 함수의 매개변수와 리턴 타입으로 모두 `Type` 을 사용하기 때문에, 함수의 타입을 비교할 때 **반공변성을 가지는 매개변수와, 공변성을 가지는 리턴 타입을 모두 만족**해야 하기 때문에, 무공변성을 가진 타입이다.

```typescript
declare const valueAsNumber: InvariantOf2<number>;
declare const valueAs1: InvariantOf2<1>;

valueAsNumber = valueAs1; // 에러!
valueAs1 = valueAsNumber; // 에러!

declare const valueAsStringOrNumber: InvariantOf2<string | number>;
declare const valueAsString: InvariantOf2<string>;

valueAsStringOrNumber = valueAsString; // 에러!
valueAsString = valueAsStringOrNumber; // 에러!
```

이제 무공변적으로 타이핑된 객체는 **'봉인된', '정확한'** 타입이므로 `Object.keys`의 리턴 타입을 구체적으로 만들 수 있다.

또한, 명목적 타입과 달리 모든 개별 타입을 위한 브랜드 함수를 만들 필요 없이, 무공변 타입을 만드는 함수 하나만 만들면 된다.

```typescript
interface AB {
  a: string;
  b: string;
}

// 무공변적 타입으로 만들어주는 함수
export function invariantOf<Type>(value: Type): InvariantOf<Type> {
  return value as InvariantOf<Type>;
}

function getKeysOfAB(arg: Invariant<AB>): (keyof AB)[] {
  return Object.keys(arg) as (keyof AB)[];
}

const invalidArgument = {
  a: 'some',
  b: 'thing',
  c: 'unexpected',
};

const validArgument = createAB({
  a: 'some',
  b: 'thing',
});

let keys: (keyof AB)[];

keys = getKeysOfAB(invalidArgument); // 에러!
keys = getKeysOfAB(validArgument);
```

### 무공변 타입을 전역에서 사용하기

타입스크립트는 [전역 보강](https://www.typescriptlang.org/ko/docs/handbook/declaration-merging.html#%EC%A0%84%EC%97%AD-%EB%B3%B4%EA%B0%95-global-augmentation)이라는 선언 병합 방법을 제공한다.

전역의 선언을 수정하는 것은 자칫 위험해 보일 수 있지만, 무공변 타입이라는 제약 안에서만 적용되므로 시도해볼 수 있다.

무공변 타입을 사용하는 경우를 위한 오버로드를 다음과 같이 전역 객체에 추가할 수 있다.

```typescript
declare global {
  export interface ObjectConstructor {
    getOwnPropertyNames<T extends object>(o: InvariantOf<T>): Array<keyof T>;

    keys<T extends object>(o: InvariantOf<T>): Array<keyof T>;

    entries<T extends object>(o: InvariantOf<T>): Array<[keyof T, T[keyof T]]>;
  }
}
```

이를 통해 객체를 순회하는 메서드에, 무공변 타입을 사용하는 경우 위의 오버로드 시그니쳐가 선택되어 더 구체적인 타입을 얻을 수 있게 된다.

```typescript
interface AB {
  a: string;
  b: string;
}

declare const ab: AB;

Object.keys(ab); // string[]
Object.keys(invariantOf(ab)); // (keyof AB)[]
```

## 마치며 ...

물론, 이 방법은 [타입스크립트의 목표](https://github.com/microsoft/TypeScript/wiki/TypeScript-Design-Goals)에 포함되는 일반적인 구조적 타입 시스템을 거스르고, 트릭적이어서 친절하지 않은 에러 메시지를 겪게 되는 단점이 있다.

따라서, 구조적 타입 시스템에 익숙해지고, 타입스크립트의 제약 안에서 객체를 순회하는 것이 더 권장된다.

그렇지만 객체의 키 속성을 구체적으로 알기 위해서는 **개발자가 어설션**해야 되는 타입스크립트의 디자인적 한계 사항에 대한 나름의 방법을 찾을 수 있었던 좋은 경험이었다.

- [사용 예제 모음 - TypeScript Playground](https://www.typescriptlang.org/play?#code/PQKhAIChwxQrsSq7CAE+QAwuFDxwIuPkDUDhKscBqrgKU3iCUPYKk90IwkAJgKYDGANgIYBOd4DA9gHYDOAF3CCWAcwBc4AK68AlgEdpnfgE8AtgCNuTANyRajVhxGqADpwAq4sXRoAeS9wDWdXgD5wAXnABvaOAcLDR8TKrgANqiYgC6Uk6uvPoAvvqQdAAeZtxswoLmnADyZixKdI4FADTgCW7eMrzOvNwA7h71lgXgAGQ1NnaOLm7uaXK8gnRsAGYsDJwAggBCfgEsUkJsY2L64OCa64KbvNuQyQb5FuAActzqYyxMS-XFpcr2S9UA5EufIwbAwHACGQ6EAPOOAHQ7wIAZzsAJy2AFtHAD8TxEAMH2AHPbADst4EAFquADCHIFNZAxBHI+FwghMlgAKFj7cBLACUUhud14Dye-l2HEE0jYvHANP5-Gut3uj0WKQMBN4RJJfNsggA0nRVPxClNFqpmaLqWxJMKWWzFozwJTXKpuFM6UaIjEVpy6NzeeBCpoAFaMQQAOjN-B1YnpgpNZotVvpNolkB4AmENIAag9lPUOfypJ9+Lc6J9KgFaZ9BAALLZZ05pKNCfmaBjxpiJnzJtbgNMZ4u7XMFovZ3YMVOyTIWIl2YupAxl4TNA1i6u1sl0FgUxbUzRTuj0tJMB3gH1SU3KkMM8MGH31eVKlVqjVa1lMRdVhMr3TgAHgQALo4Ab9oAhJAjz4T8rVerNRFK9KXHUUlmXVd-jAKAYHAQAWbsAV5rAAGekFMBwAhiHIShqEgJ9AGqZ8BAAiewAPyfAQBECcAH9rcMBPscjyLoAEleAAN3YOQWHGNUKkuTIJl4GghW4N0PU8Z4SjKbi6GqYNLU6Cw-kgC5OCY1jNg4wQAAU2G4CxclUSTPB8P14gKAMvE8OS6DSJTwBUtj1IAZTkMRWUdcpLMMu1AlnEJeDCSJojiWyWPs8YtJ0yZ8gMlI0ifQAFFqI0jKPSLI6NMS47LUzipgM3YfEsnpgtU9jxicly5x5dyCgUp9EJQ1A0AhaF4SRbE8Vo3JwClGVSTGYr1K4jzKVYms6BMixjUykrBEG6qvK5Hk+RGxMWCFKaBpyjyI264lSV-M8pipdg9XW7L3kWdxjR3c1LX3W1kwWp0XXdIlvT-P0A1WoNd1u60YgjUdwD60KZsOxZl3qYGstBxcILSb9wH2-8jsrOHH0BN9PwRpG1SpKHptx8G70gwxmHYTgxCYISHi8jrhDGCZplmIphKJABhPgNmkIkci83Z5UKNpwt0-IrhYdQ6H4RxwF4twBPAISXsEdxKW4KRTtBxxLqkeY2DYFh9JkmoFN2XYfWl2X+ME1nldV9WQuhwbtbpPWDfsI3LBN023EOORJYtjI+PlxWRLtoqQad41df1-SIg96pLDjn6ahiGI-l2M4zkgBnJhmOYrS8hsNi2HY9gOI4TizwHi+OaODeeG23pVWHiYfJ8a7EG1I054QzUJuvwh8Z6PSb318Y2lvRvpAMn0pT4WE+cAAB9G00T4wxiAwgA)
- [구현 레포지토리 - younho9/invariant-of](https://github.com/younho9/invariant-of)
- [테스트 케이스 모음](https://github.com/younho9/invariant-of/blob/main/index.test-d.ts)

## 참고자료

### 객체의 키를 순회하는 방법

- https://fettblog.eu/typescript-better-object-keys/
- https://effectivetypescript.com/2020/05/26/iterate-objects/
- https://github.com/microsoft/TypeScript/pull/12253#issuecomment-263132208

### 타입 호환성

- https://flow.org/en/docs/lang/variance/
- https://basarat.gitbook.io/typescript/type-system/type-compatibility#variance
- https://basarat.gitbook.io/typescript/main-1/nominaltyping#using-interfaces
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/seal

### 명목적 타입(또는 불투명 타입)

- https://codemix.com/opaque-types-in-javascript/
- https://blog.beraliv.dev/2021-05-07-opaque-type-in-typescript
- https://github.com/sindresorhus/type-fest/blob/main/source/opaque.d.ts
