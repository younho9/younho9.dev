---
hero: ./images/2021-08-28-type-guard-and-overload-image-1.jpeg
slug: 'type-guard-and-overloads'
title: '타입 가드 함수와 오버로드'
date: 2021-08-28
tags: ['TypeScript']
author: younho9
excerpt: 타입스크립트를 사용하다보면, 타입 가드 함수를 사용해서 타입의 범위를 좁혀야 하는 경우가 생긴다. 그런데, 타입 가드 함수를 하나 둘씩 추가하다 보니, 같은 기능의 함수가 중복되어 생성되는 경우가 있었다.
---

## TL;DR

- 중복되는 타입 가드 함수에 오버로드를 사용해보자.
- 오버로드가 있는 함수는 타입 추론 시 적용 가능한 첫 번째 시그니쳐가 선택된다.
- 오버로드 시그니쳐을 작성할 때는 순서가 중요하다. 구체적 타입 > 일반적 타입 순서로 작성한다.
- 타입 가드 함수 자체를 인자로 사용할 때(ex. `Array.filter`) 컴파일러의 함수 추론에 문제가 있는 경우, 명시적으로 타입 인자를 넘겨 사용한다.

## Intro

타입스크립트를 사용하다보면, 타입 가드 함수를 사용해서 [타입의 범위를 좁혀야 하는](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) 경우가 생긴다.

그런데, 타입 가드 함수를 하나 둘씩 추가하다 보니, 같은 기능의 함수가 중복되어 생성되는 경우가 있었다.

## Example

```typescript
interface Coffee {
  type: 'coffee';
}

interface CoffeeInfo extends Coffee {
  price: number;
  caffeine: number;
}

interface CoffeeDetailInfo extends CoffeeInfo {
  coffeeBean: string;
}

interface Ade {
  type: 'ade';
}

interface AdeInfo extends Ade {
  price: number;
  sugar: number;
}

interface AdeDetailInfo extends AdeInfo {
  fruit: string;
}

type Drink = Coffee | Ade;
type DrinkInfo = CoffeeInfo | AdeInfo;
type DrinkDetailInfo = CoffeeDetailInfo | AdeDetailInfo;
```

`Coffee` 를 확장한 `CoffeeInfo`와 `CoffeeInfo`를 확장한 `CoffeeDetailInfo` 가 있고, `Ade` 를 확장한 `AdeInfo`와 `AdeInfo`를 확장한 `AdeDetailInfo` 가 있는 상황이다.

어떤 API에서 커피 또는 에이드의 정보를 묶어서 "음료 정보"로 전달하고, 어떤 API에서는 커피 또는 에이드의 상세 정보를 묶어서 "음료 상세 정보"로 전달한다.

"음료 정보" 중에서 "커피 정보"를 찾기 위한 타입 가드 함수와, "음료 상세 정보" 중에서 "커피 상세 정보"를 찾기 위한 타입 가드 함수를 다음과 같이 작성했다.

```typescript
function isCoffeeInfo(value: DrinkInfo): value is CoffeeInfo {
  return value.type === 'coffee';
}

function isCoffeeDetailInfo(value: DrinkDetailInfo): value is CoffeeDetailInfo {
  return value.type === 'coffee';
}
```

이제 이 함수들을 사용해서 "커피 정보"와 "커피 상세 정보"를 안전하게 사용할 수 있게 되었다.

```typescript
function getCaffeine(value: DrinkInfo): number {
  if (isCoffeeInfo(value)) {
    // (parameter) value: CoffeeInfo
    return value.caffeine;
  }

  return 0;
}

function getCoffeeBean(value: DrinkDetailInfo): string | null {
  if (isCoffeeDetailInfo(value)) {
    // (parameter) value: CoffeeDetailInfo
    return value.coffeeBean;
  }

  return null;
}
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwig3gKGWTAE8AHCALmQHIFNsIaBufAX331ElkRQyw4AkiBjpkEAB6QQAEwDOaBjmQEiZKMCTUQAVwC2AI2isiCOINBVkeoyfadu0eEiWCIAEQhg4wADYiYhLSEHKKAoyB4mrI9O4AQhBwINTyYJogAOasHFzgznzIAIKyeITE5NY0cKUsDnk8LiglEFHBMgrFparlGlrWtsZQpsjyuplwUDoGQzmO+byuLV4+-m1SHYotbTEwULrAYKnpoNn1pBTIHhkA1sgAvG6MyAA+XRCsFyjXoDdtjxFhKJxG9tsDPpUrrcVr4AsCHk8cDC1vDQaVkXCxKx8DBdCAEGBgOgQMhgPJAa1gQAKcoANzgfl01h+ID+wPwAEpqPTGSgyYjKUEYlBvLooCSeUyAHRfB73R50ZRMOY4vEEokkskUjFRGlESXM6HeWFRTnchlM0nhJU6+HC0Xi5AGmWQ+UKuKMOq5XH4wnE5CZbyoCzYKxUg3UFlssRcmwzaA9IjAGDIKlapW6g0cjmJojIAD0+dTZEmcH03mgOYjAtNeeQIrAYolFogUvMlhAH3KuSIDabyAADCqfer-YGwBTEslwy3I0bVpj0LG0hlMq8434-Lnk6n0+5bWIZ7zs7miIXi6Xyzwq7OBQf0OVew7m7y20qpyARj368+N34ckAA)

그런데 `isCoffeeInfo`와 `isCoffeeDetailInfo`는 함수 시그니쳐만 다를 뿐, 함수의 기능은 같다.

자바스크립트를 사용했다면, 굳이 작성하지 않아도 될 함수가 하나 늘어난 것 같다.

같은 기능의 함수인데, 하나로 줄일 순 없을까?

## 첫 번째 시도: 제네릭

타입스크립트에는 [제네릭](https://www.typescriptlang.org/docs/handbook/2/generics.html)이라는 기능이 있다. 이를 활용하면 타입 변수를 사용할 수 있다.

```typescript
function isCoffee<U extends T, T extends Drink = Drink>(value: T): value is U {
  return value.type === 'coffee';
}

function getCaffeine(value: DrinkInfo): number {
  if (isCoffee<CoffeeInfo>(value)) {
    // (parameter) value: CoffeeInfo
    return value.caffeine;
  }

  return 0;
}
function getCoffeeBean(value: DrinkDetailInfo): string | null {
  if (isCoffee<CoffeeDetailInfo>(value)) {
    // (parameter) value: CoffeeDetailInfo
    return value.coffeeBean;
  }

  return null;
}
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwig3gKGWTAE8AHCALmQHIFNsIaBufAX331ElkRQyw4AkiBjpkEAB6QQAEwDOaBjmQEiZKMCTUQAVwC2AI2isiCOINBVkeoyfadu0eEiWCIAEQhg4wADYiYhLSEHKKAoyB4mrI9O4AQhBwINTyYJogAOasHFzgznzIAIKyeITE5NY0cKUsDnk8LiglEFHBMgrFparlGlrWtsZQpsjyuplwUDoGQzmO+byuLV4+-m1SHYotbTEwULrAYKnpoNn1pBTIHhkA1sgAvG6MyAA+XRCsFyjXoDdtjxFhKJxG9tsDPpUrrcVr4AsCHk8cDC1vDQaVkXCxKx8DBdCAEGBgOgQMhgPJARAADzlACq7VCnQAKgAacqM+lhKG-BE-EA3fAAPgAFAA3OB+XTWRkASmoYolKDJyDpMSg3l0UBJ8slADovg97o86MomHMcXiCUSSZlvKgLNgrKLxZLqLy-sDZTYZtAekRgDBkEKyRTKRSosLtRBpdLfURkAB6eOBsiTOD6bzQGOR6hh4HlIhqsAarXOiA68yWEAfcq5AvqzXIAAMc1x+MJxOQNrAFMSySdCtd0O8sKinrSGUyry9fj8sf9geDJtDJox4f7kujsaIieTqfTPCzpZzK+HKLE+eQheLyEj5ZNvZAI1rl-rJL0M5yQA)

`isCoffee`라는 함수를 만들고, 두 번째 타입 매개변수인 `T`를 `Drink`를 확장해야 한다는 제약과 기본값으로 두고, 첫 번째 타입 매개변수인 `U`를 `T`를 확장해야 한다는 제약을 두어서, 첫 번째 타입 매개변수로 받은 타입 임을 가드하게 했다.

이렇게 하니, 하나의 함수로 "커피 정보"와 "커피 상세 정보"를 안전하게 사용할 수 있게 되었다.

하지만, 함수를 호출할 때마다, 명시적인 타입을 인수로 전달을 해줘야 하는 번거로움이 있다.

타입스크립트 컴파일러가 전달하는 인수에 따라 추론할 수 있게 작성하는 방법은 없을까?

## 두 번째 시도: 제네릭과 조건부 타입

타입스크립트에는 [조건부 타입](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html)이라는 기능이 있다. 이를 활용하면 타입스크립트 컴파일러가 타입을 조건에 따라 추론하게끔 할 수 있다.

```typescript
type CoffeeOf<T> = T extends DrinkDetailInfo
  ? CoffeeDetailInfo
  : T extends DrinkInfo
  ? CoffeeInfo
  : T extends Drink
  ? Coffee
  : never;

// Coffee
type A = CoffeeOf<Drink>;
// CoffeeInfo
type B = CoffeeOf<DrinkInfo>;
// CoffeeDetailInfo
type C = CoffeeOf<DrinkDetailInfo>;
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwig3gKGWTAE8AHCALmQHIFNsIaBufAX331ElkRQyw4AkiBjpkEAB6QQAEwDOaBjmQEiZKMCTUQAVwC2AI2isiCOINBVkeoyfadu0eEiWCIAEQhg4wADYiYhLSEHKKAoyB4mrI9O4AQhBwINTyYJogAOasHFzgznzIAIKyeITE5NY0cKUsDnk8LiglEFHBMgrFparlGlrWtsZQpsjyuplwUDoGQzmO+byuLV4+-m1SHYotbTEwULrAYKnpoNn1pBTIHhkA1sgAvG6MyAA+XRCsFyjXoDdtjxFhKJxG9tsDPpUrrcVr4AsCHk8cDC1vDQaVkXCxKx8F9ERAAPIwAA8ABUAHwIkntUKdH4gG4YqLlAD8eMZwPK1CpGxpijpfw5RFZgNaguQXOpYShvxZeM5NggADd7PgAPSquW4ooIkWEon8smsdV4pm4+I65QE4n8qKGtUakXssQ4yGoC3uPX8p3oQ1AA)

`CoffeeOf<T>`은 타입 매개변수로 받은 `T`가 "음료 상세 정보"면, "커피 상세 정보", "음료 정보"면, "커피 정보", "음료 기본"이면 "커피 기본", 그리고 무엇도 아니면 `never`인, 요약하면 "커피 응답"을 찾아주는 타입이다.

조건부 타입을 작성할 때 주의사항은, 일반적인 삼항연산자처럼 조건에 부합하는 경우 즉시 리턴되므로, 좁은 범위의 타입부터 작성해야 정상적으로 타입을 추론할 수 있다는 것이다.

아래의 경우처럼, `Drink`부터 조건문을 작성할 경우, 아래의 모든 타입이 `Drink`를 확장하기 때문에, 모든 타입을 `Coffee`로 추론하게 된다.

```typescript
type CoffeeOf<T> = T extends Drink
  ? Coffee
  : T extends DrinkInfo
  ? CoffeeInfo
  : T extends DrinkDetailInfo
  ? CoffeeDetailInfo
  : never;

// Coffee
type A = CoffeeOf<Drink>;
// Coffee
type B = CoffeeOf<DrinkInfo>;
// Coffee
type C = CoffeeOf<DrinkDetailInfo>;
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2&ssl=44&ssc=36&pln=31&pc=1#code/JYOwLgpgTgZghgYwgAgMIHsYwig3gKGWTAE8AHCALmQHIFNsIaBufAX331ElkRQyw4AkiBjpkEAB6QQAEwDOaBjmQEiZKMCTUQAVwC2AI2isiCOINBVkeoyfadu0eEiWCIAEQhg4wADYiYhLSEHKKAoyB4mrI9O4AQhBwINTyYJogAOasHFzgznzIAIKyeITE5NY0cKUsDnk8LiglEFHBMgrFparlGlrWtsZQpsjyuplwUDoGQzmO+byuLV4+-m1SHYotbTEwULrAYKnpoNn1pBTIHhkA1sgAvG6MyAA+XRCsFyjXoDdtjxFhKJxG9tsDPpUrrcVr4AsCHk8cDC1vDQaVkXCxKx8F9ERAAPIwAA8ABUAHwIkntUKdH4gG7lAD8ePK1CpGxpijpf2BTLxUVZyHZITCUN+GIFRGZgM83lhkuQOggADd7PgAPTqlm4ooImWEoncsmsTXayHxPXKAnE7lRY0arUynGQ1CW9wG7kS4HGoA)

이를 사용해 인자의 조건에 따라 "커피 응답"을 찾을 수 있게 되었다.

그럼 이를 타입 가드 함수에 적용해볼 수 있을까?

"음료 기본 응답"을 확장하는 인자의 타입을 가지고, 인자의 조건에 맞는 "커피 응답"을 찾아서 인자가 조건에 부합하는 "커피 응답"임을 가드해주는 함수를 작성했다.

```typescript
function isCoffee<T extends Drink>(value: T): value is CoffeeOf<T> {
  return value.type === 'coffee';
}
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwig3gKGWTAE8AHCALmQHIFNsIaBufAX331ElkRQyw4AkiBjpkEAB6QQAEwDOaBjmQEiZKMCTUQAVwC2AI2isiCOINBVkeoyfadu0eEiWCIAEQhg4wADYiYhLSEHKKAoyB4mrI9O4AQhBwINTyYJogAOasHFzgznzIAIKyeITE5NY0cKUsDnk8LiglEFHBMgrFparlGlrWtsZQpsjyuplwUDoGQzmO+byuLV4+-m1SHYotbTEwULrAYKnpoNn1pBTIHhkA1sgAvG6MyAA+XRCsFyjXoDdtjxFhKJxG9tsDPpUrrcVr4AsCHk8cDC1vDQaVkXCxKx8F9ERAAPIwAA8ABUAHwIkntUKdH4gG4YqLlAD8eMZwPK1CpGxpijpfw5RFZgNaguQXOpYShvxZeM5NggADd7PgAPSquW4ooIkWEon8smsdV4pm4+I65QE4n8qKGtUakXssQ4yGoC3uPX8p3oO34GC6EAIMDAdAgZDAeQi0mS2m3MkACnKirgfl01hJ+AAlNRk6mUBG8XryT0iFBvLooGHc2mAHS4+4N2hxRh1NhAA)

하지만, 이 함수는 에러가 발생한다.

```typescript
// A type predicate's type must be assignable to its parameter's type.
//   Type 'CoffeeOf<T>' is not assignable to type 'T'.
//     'CoffeeOf<T>' is assignable to the constraint of type 'T', but 'T' could be instantiated with a different subtype of constraint 'Drink'.
```

이것은 [제네릭 타입 매개변수에 제네릭 제약조건 타입을 할당할 수 없다는 에러](https://github.com/Microsoft/TypeScript/issues/29049)로, 아래의 함수에서도 동일한 에러가 발생한다.

```typescript
// Type 'string' is not assignable to type 'T'.
//   'string' is assignable to the constraint of type 'T', but 'T' could be instantiated with a different subtype of constraint 'string'.
function fn1<T extends string>(x: T): T {
  return 'hello world!';
}
```

즉, 제네릭 타입 매개변수 `T`의 제약사항인 `T extends string`은 **`T`가 `string` 타입 이다**를 뜻하는 것이 아니라, **`T`가 `string` 타입의 서브타입이다**라는 뜻이고, 서브타입에 슈퍼타입을 할당할 수 없기 때문에 에러가 발생하는 것이다.

이 규칙은 타입 가드 함수의 [술어 부분(predicate)](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates)에서도 적용되어, 추론하는 타입 역시 파라미터에 "할당 가능"해야 한다는 제약이 있다.

결국, 조건부 타입을 사용해서, 전달하는 인자의 타입으로 가드할 타입을 추론하게 끔하는 방법을 찾지 못했다.

그러면 항상 첫 번째 방법처럼, 명시적인 타입을 타입 인수로 전달해주면서 사용해야 할까?

## 세 번째 시도: 함수 오버로딩

다시 처음 문제의 원인을 생각해보자.

> `isCoffeeInfo`와 `isCoffeeDetailInfo`는 함수 시그니쳐만 다를 뿐, 함수의 기능은 같다.

**"함수 기능은 같은데 시그니쳐만 다르다"**는 것이 문제의 원인이었다. 사실 이를 위한 타입스크립트의 기능은 [함수 오버로드](https://www.typescriptlang.org/docs/handbook/2/functions.html#function-overloads)이다.

```typescript
function isCoffee(value: DrinkDetailInfo): value is CoffeeDetailInfo;
function isCoffee(value: DrinkInfo): value is CoffeeInfo;
function isCoffee(value: Drink): value is Coffee {
  return value.type === 'coffee';
}
```

오버로드 함수는 [오버로드 시그니쳐와 구현 시그니쳐](https://www.typescriptlang.org/docs/handbook/2/functions.html#overload-signatures-and-the-implementation-signature)로 구성된다.

자바스크립트에서 오버로드는 인자의 조건(타입과 갯수)에 따른 분기를 함수 내부에 작성하는 방법이기 때문에, 타입스크립트에서도 오버로드 함수는 모든 오버로드 시그니쳐를 커버할 수 있는 하나의 구현 시그니쳐를 작성해야 한다.

구현 시그니쳐는 가장 아래에 위치하고, 나머지 오버로드 함수 시그니쳐와 호환되어야 한다.

따라서 `isCoffee`의 구현 시그니쳐에는 "음료 응답"의 가장 넓은 범위의 타입인 `Drink`를 인자의 타입으로 갖고, "커피 응답"의 가장 넓은 범위의 타입인 `Coffee`를 술어 부분의 추론 타입으로 작성했다.

그리고 나머지 두 오버로드 시그니쳐의 인자 타입인 `DrinkInfo`과 `DrinkDetailInfo`는 `Drink`에 호환되고 술어 부분의 추론 타입인 `CoffeeInfo`과 `CoffeeDetailInfo`는 `Coffee`에 호환된다.

```typescript
function getCaffeine(value: DrinkInfo): number {
  if (isCoffee(value)) {
    // (parameter) value: CoffeeInfo
    return value.caffeine;
  }

  return 0;
}

function getCoffeeBean(value: DrinkDetailInfo): string | null {
  if (isCoffee(value)) {
    // (parameter) value: CoffeeDetailInfo
    return value.coffeeBean;
  }

  return null;
}
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwig3gKGWTAE8AHCALmQHIFNsIaBufAX331ElkRQyw4AkiBjpkEAB6QQAEwDOaBjmQEiZKMCTUQAVwC2AI2isiCOINBVkeoyfadu0eEiWCIAEQhg4wADYiYhLSEHKKAoyB4mrI9O4AQhBwINTyYJogAOasHFzgznzIAIKyeITE5NY0cKUsDnk8LiglEFHBMgrFparlGlrWtsZQpsjyuplwUDoGQzmO+byuLV4+-m1SHYotbTEwULrAYKnpoNn1pBTIHhkA1sgAvG6MyAA+XRCsFyjXoDdtjxFhKJxG9tsDPpUrrcVr4AsCHk8cDC1vDQaVkXCxKx8DBdCAEGBgOgQMhgPJARAABQANzgfl01h+IBuGKiAEpqLT6SgyYjPN5YVFWLj8YTiaTycoqVyGdQmX9gRzkDKeeEpUKcXiCUSSWSKTS6bKob8lSqJXyekQoN5dFASSqAHRfB73R50KV1XIi7XizLeVAWbBWA3cuW3dnTOxQS2kmDISl6qUhhlstkxogAegz8bIkzg+m80DTKuoFKi5StNrtysNEAd5ksIA+5VylbAtpJAAY5prRTrkH6wBTEslk4zoQKUWIlWkMplXjZdH4-DHgHGE5L3GPU+nkFmc3mCzxi7XS1LWcCK8hre3q464owRyARq3r1WSXplzkgA)

이제 하나의 함수 `isCoffee` 만으로, 타입 인자를 명시적으로 전달하지 않고 타입스크립트가 전달 받는 인자의 타입으로 추론할 수 있게 되었다.

오버로드 함수는 컴파일되면 하나의 함수만 남기 때문에, 기존에 같은 기능을 하는 함수가 여러 개 존재하는 것보다 번들사이즈를 줄일 수 있다.

그리고 같은 기능의 함수가 여러 개 있는 것보다 유지보수하기 쉬워진다.

### 함수 오버로딩에서의 유의사항

함수 오버로딩에서 오버로드 시그니쳐의 순서는 중요하다.

적용 가능한 첫 번째 오버로드 시그니쳐가 선택되기 때문에, 조건부 타입을 작성할 때 처럼, 보다 [구체적인 서명을 먼저 배치](https://github.com/microsoft/TypeScript/issues/1860#issuecomment-72154737)해야 한다.

그리고 `Array.filter`에서 오버로드 함수 자체가 인자로 사용될 때는 올바른 오버로드 시그니쳐를 추론하지 못하는 문제가 있었다.

```typescript
// 시그니쳐 (1)
function isCoffee(value: DrinkDetailInfo): value is CoffeeDetailInfo;
// 시그니쳐 (2)
function isCoffee(value: DrinkInfo): value is CoffeeInfo;
function isCoffee(value: Drink): value is Coffee {
  return value.type === 'coffee';
}

declare const drinkInfos: DrinkInfo[];
// 시그니쳐 (1)이 뒤에 올 때 에러가 발생함.
drinkInfos.filter(isCoffee).map((value) => value.caffeine);

declare const drinkDetailInfos: DrinkDetailInfo[];
// 시그니쳐 (2)가 뒤에 올 때 에러가 발생함.
drinkDetailInfos.filter(isCoffee).map((value) => value.coffeeBean);
```

> `시그니쳐 (1)`과 `시그니쳐 (2)`의 순서가 바뀔 때마다, 에러의 위치가 달라진다.

이런 케이스에서는 올바른 유형을 추론하기 위해 타입스크립트 컴파일러의 추론에 의존할 수 없는 경우이므로, `Array.filter`에 명시적으로 타입 인자를 넘겨주는 것으로 사용할 수 있다.

```typescript
declare const drinkInfos: DrinkInfo[];
drinkInfos.filter<CoffeeInfo>(isCoffee).map((value) => value.caffeine);

declare const drinkDetailInfos: DrinkDetailInfo[];
drinkDetailInfos
  .filter<CoffeeDetailInfo>(isCoffee)
  .map((value) => value.coffeeBean);
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwig3gKGWTAE8AHCALmQHIFNsIaBufAX331ElkRQyw4AkiBjpkEAB6QQAEwDOaBjmQEiZKMCTUQAVwC2AI2isiCOINBVkeoyfadu0eEiWCIAEQhg4wADYiYhLSEHKKAoyB4mrI9O4AQhBwINTyYJogAOasHFzgznzIAIKyeITE5NY0cKUsDnk8LiglEFHBMgrFparlGlrWtsZQpsjyuplwUDoGQzmO+byuLV4+-m1SHYotbTEwULrAYKnpoNn1pBTIHhkA1sgAvG6MyAA+XRCsFyjXoDdtjxFhKJxG9tsDPpUrrcVr4AsCHk8cDC1vDQaVkXCxKx8AB6HHIQA7Q4AP2sAE02ABZnkAAKACMAEp8DBdCAEGBgOgQMhgPJARBKQA3OB+XTWH4gG4YqK06gCoUoLmIzzeWFRVh4wmkimUgBM9MZzNZ7M53OUvJlwuoor+wKlyDNcvCJpVDKZLLZHK5PP5gvNUN+NrtRoVPSIUG8uigHLtADovg97o86Ca6rlSgg-JMUPQQGlkLJblF5Bb88CANoAXVx+OJ5KpdMALuPIQAlLYAF0eQgBox5CAGVbkM3ADftgAAa5CAHB7ALsDgAtVqP4PO-AtRmD+HiUj0m2lR-RwMiUr2y2kPAB8tu9ECj5ksIAg9KnEDTGdi7Jz07FEuBhd9T6VKLE5cr6pr2tpg4tu2XY9gOw7jpOj7ih+mLoPIc4LtAS7Gu4q7rpu27Cru9wHtGcSMIkySXmqgAkY4AIT2ADodgA7Lb+ZKAD6dyCACG9gA1nYAEauACLjIF9uBgAaq4AA5PIIAUqOADLjk56q6hrLu4USYSKxZiP6R6BjyOzlKGYDhpGR4xpC8YJvhODJpwUGzvOfiLlJkTWmuG5bna2G4dpp7YFYl7iQa7ooYwz5iLJRa-D56CKbKykmoFwbIOpmmHrKOmXHptAGUwcxTtCMGmYhUDITygVobZskOTFwoniahEgMR+KAKFdBKAIATyCAAMLgCh48ggAe44ACePIIAIBOADdNqUzi+5QIeZ0AADwqcCe7ZSug3oXZR6FXhFgueetLYlBgXyINZk8GNYXpRNU2oTN+X2fuRXHklZWrUAA)

## 참고자료

- https://www.typescriptlang.org/docs/handbook/2/narrowing.html
- https://www.typescriptlang.org/ko/docs/handbook/2/generics.html
- https://www.typescriptlang.org/docs/handbook/2/conditional-types.html
- https://www.typescriptlang.org/docs/handbook/2/functions.html#function-overloads
