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
interface CoffeeBaseResponse {
  type: 'coffee';
}

interface CoffeeInfoResponse extends CoffeeBaseResponse {
  price: number;
  caffeine: number;
}

interface CoffeeDetailInfoResponse extends CoffeeInfoResponse {
  coffeeBean: string;
}

interface AdeBaseResponse {
  type: 'ade';
}

interface AdeInfoResponse extends AdeBaseResponse {
  price: number;
  sugar: number;
}

interface AdeDetailInfoResponse extends AdeInfoResponse {
  fruit: string;
}

type DrinkBaseResponse = CoffeeBaseResponse | AdeBaseResponse;
type DrinkInfoResponse = CoffeeInfoResponse | AdeInfoResponse;
type DrinkDetailInfoResponse = CoffeeDetailInfoResponse | AdeDetailInfoResponse;
```

`CoffeeBaseResponse` 를 확장한 `CoffeeInfoResponse`와 `CoffeeInfoResponse`를 확장한 `CoffeeDetailInfoResponse` 가 있고, `AdeBaseResponse` 를 확장한 `AdeInfoResponse`와 `AdeInfoResponse`를 확장한 `AdeDetailInfoResponse` 가 있는 상황이다.

어떤 API에서 커피 또는 에이드의 정보를 묶어서 "음료 정보"로 전달하고, 어떤 API에서는 커피 또는 에이드의 상세 정보를 묶어서 "음료 상세 정보"로 전달한다.

"음료 정보" 중에서 "커피 정보"를 찾기 위한 타입 가드 함수와, "음료 상세 정보" 중에서 "커피 상세 정보"를 찾기 위한 타입 가드 함수를 다음과 같이 작성했다.

```typescript
function isCoffeeInfoResponse(
  response: DrinkInfoResponse
): response is CoffeeInfoResponse {
  return response.type === 'coffee';
}

function isCoffeeDetailInfoResponse(
  response: DrinkDetailInfoResponse
): response is CoffeeDetailInfoResponse {
  return response.type === 'coffee';
}
```

이제 이 함수들을 사용해서 "커피 정보"와 "커피 상세 정보"를 안전하게 사용할 수 있게 되었다.

```typescript
function getCaffeine(response: DrinkInfoResponse): number {
  if (isCoffeeInfoResponse(response)) {
    // (parameter) response: CoffeeInfoResponse
    return response.caffeine;
  }

  return 0;
}

function getCoffeeBean(response: DrinkDetailInfoResponse): string | null {
  if (isCoffeeDetailInfoResponse(response)) {
    // (parameter) response: CoffeeDetailInfoResponse
    return response.coffeeBean;
  }

  return null;
}
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwhAQnAZwgCUICAHdEI5AbwChlkwBPciALmQHIFNsI3ANz0AvvXqhIsRCgxYcASRAx0pClRoQAHpBAATAmn458RdZWooGTclGBIuIAK4BbAEbQRTBHAWhOZBcPLzEJKWh4JGMFCAARCDA4YAAbZVULTRQdPUMYgXS1MksaG2Q+WNwIOBAuAjB7EABzEXFJcEjZZABBfTxCEmKsukZmNkDuOD7hMPbpKJReiELMq2QciAMjJbNBjTWyuwdA4M8ob2QCZya4KCc3M9bwjplopYSk1JWhtY2tnr6332pVGMCgzmAYDqDVALVmrHYyDijQA1rtVjQALz5UwDDEoAA+AP65h+RBECJQyNAKKBJRQ2PkBRURWBhOJdKyFPGSNRH2SaRZ+OQjJM8USAs5ayJ7wlXyFZIgInoMGcIAQYGAVGQwAITKUCrZAApRlBFVxqSBaYb6fQAJRcM1snVGfXLG3DMpmsDOKAgZBO+kAOkpIsx2N4YpmbVV6s12t1bv58oyipNTEDWQtfLlgtTbPtjsVLpx4s+edZ9JGGcSvv9masIZ54YjFQE0YksY1Wv9TUSqD82ACRobRGzNKlRAdQQe0GrOpgyCNibFk4gI8Vdrt86YAHpd0vyLc4K5EtBt6PAm616Maz6-QHFUHfP4QErRm073XkAAGJ4qtVu21PswDdKoag3NlxytZMK3xad6kaJpkCJFwUhSedgEXZc9TFWC10g+ktx3ZB90PY9T2kC9zVLfCPSsW9H3vesnzbUxqhAC5PyY780JSVogA)

그런데 `isCoffeeInfoResponse`와 `isCoffeeDetailInfoResponse`는 함수 시그니쳐만 다를 뿐, 함수의 기능은 같다.

자바스크립트를 사용했다면, 굳이 작성하지 않아도 될 함수가 하나 늘어난 것 같다.

같은 기능의 함수인데, 하나로 줄일 순 없을까?

## 첫 번째 시도: 제네릭

타입스크립트에는 [제네릭](https://www.typescriptlang.org/docs/handbook/2/generics.html)이라는 기능이 있다. 이를 활용하면 타입 변수를 사용할 수 있다.

```typescript
function isCoffeeResponse<
  U extends T,
  T extends DrinkBaseResponse = DrinkBaseResponse
>(response: T): response is U {
  return response.type === 'coffee';
}

function getCaffeine(response: DrinkInfoResponse): number {
  if (isCoffeeResponse<CoffeeInfoResponse>(response)) {
    // (parameter) response: CoffeeInfoResponse
    return response.caffeine;
  }

  return 0;
}
function getCoffeeBean(response: DrinkDetailInfoResponse): string | null {
  if (isCoffeeResponse<CoffeeDetailInfoResponse>(response)) {
    // (parameter) response: CoffeeDetailInfoResponse
    return response.coffeeBean;
  }

  return null;
}
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwhAQnAZwgCUICAHdEI5AbwChlkwBPciALmQHIFNsI3ANz0AvvXqhIsRCgxYcASRAx0pClRoQAHpBAATAmn458RdZWooGTclGBIuIAK4BbAEbQRTBHAWhOZBcPLzEJKWh4JGMFCAARCDA4YAAbZVULTRQdPUMYgXS1MksaG2Q+WNwIOBAuAjB7EABzEXFJcEjZZABBfTxCEmKsukZmNkDuOD7hMPbpKJReiELMq2QciAMjJbNBjTWyuwdA4M8ob2QCZya4KCc3M9bwjplopYSk1JWhtY2tnr6332pVGMCgzmAYDqDVALVmrHYyDijQA1rtVjQALz5UwDDEoAA+AP65h+RBECJQyNAKKBJRQ2PkBRURWBhOJdKyFPGSNRH2SaRZ+OQjJM8USAs5ayJ7wlXyFZIgInoMGcIAQYGAVGQwAITJw+IAPKMAKrrXSbPIAFQANKMrebckZqSA0XjFSLeTT0Yr6AA+AAUUEVXCtAEouMG2TqjGaysGwM4oCBkFH6QA6SkizHY3himZtVXqzXapqJVB+bABIMhr2uqVECNBB7QEZMYAwZAB3X6vb0w29hsQQNprJhsNtpjIAD00675FucFciWgE9HVi4g4VbNGTATSZT66I6d8-hAStGbT3iQPyAADE8ixqtSmy2Be1UajW2VwXSj+fKGSKk29SNE0yBEi4KQpJOHZdj2YpGr2AGCkBbIjsBE5lEws7zouy7SGutbIXKqGsvSu6pjeyZUWyJ5ip+IAXFeVGJjRUEpK0QA)

`isCoffeeResponse`라는 함수를 만들고, 두 번째 타입 매개변수인 `T`를 `DrinkBaseResponse`를 확장해야 한다는 제약과 기본값으로 두고, 첫 번째 타입 매개변수인 `U`를 `T`를 확장해야 한다는 제약을 두어서, 첫 번째 타입 매개변수로 받은 타입 임을 가드하게 했다.

이렇게 하니, 하나의 함수로 "커피 정보"와 "커피 상세 정보"를 안전하게 사용할 수 있게 되었다.

하지만, 함수를 호출할 때마다, 명시적인 타입을 인수로 전달을 해줘야 하는 번거로움이 있다.

타입스크립트 컴파일러가 전달하는 인수에 따라 추론할 수 있게 작성하는 방법은 없을까?

## 두 번째 시도: 제네릭과 조건부 타입

타입스크립트에는 [조건부 타입](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html)이라는 기능이 있다. 이를 활용하면 타입스크립트 컴파일러가 타입을 조건에 따라 추론하게끔 할 수 있다.

```typescript
type CoffeeResponseOf<T> = T extends DrinkDetailInfoResponse
  ? CoffeeDetailInfoResponse
  : T extends DrinkInfoResponse
  ? CoffeeInfoResponse
  : T extends DrinkBaseResponse
  ? CoffeeBaseResponse
  : never;

// CoffeeBaseResponse
type CoffeeBase = CoffeeResponseOf<DrinkBaseResponse>;
// CoffeeInfoResponse
type CoffeeInfo = CoffeeResponseOf<DrinkInfoResponse>;
// CoffeeDetailInfoResponse
type CoffeeDetail = CoffeeResponseOf<DrinkDetailInfoResponse>;
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwhAQnAZwgCUICAHdEI5AbwChlkwBPciALmQHIFNsI3ANz0AvvXqhIsRCgxYcASRAx0pClRoQAHpBAATAmn458RdZWooGTclGBIuIAK4BbAEbQRTBHAWhOZBcPLzEJKWh4JGMFCAARCDA4YAAbZVULTRQdPUMYgXS1MksaG2Q+WNwIOBAuAjB7EABzEXFJcEjZZABBfTxCEmKsukZmNkDuOD7hMPbpKJReiELMq2QciAMjJbNBjTWyuwdA4M8ob2QCZya4KCc3M9bwjplopYSk1JWhtY2tnr6332pVGMCgzmAYDqDVALVmrHYyDijQA1rtVjQALz5UwDDEoAA+AP65h+RBECJQyNAKKBJRQ2PkBRURWBhOJdKyFPGSNRH2SaRZ+OQjJM8USAs5ayJ7wlXyFZIgInolJxe3pAHkYAAeAAqAD4RchdetdJs8tSQCj+fKMorRgB+NU2wV2tmjLgmv4W1FSoiOtV+iAe42m3JGS1ovH2phOpm40nuphOCAAN1C9AA9Jm1ej7ar4ySGWr8VrtZG82z9SJs4GFe6C2LCkbC6WdZGg9WsznCy6gyqeb25SkW2K2+W+cPOyIgA)

`CoffeeResponseOf<T>`은 타입 매개변수로 받은 `T`가 "음료 상세 정보"면, "커피 상세 정보", "음료 정보"면, "커피 정보", "음료 기본"이면 "커피 기본", 그리고 무엇도 아니면 `never`인, 요약하면 "커피 응답"을 찾아주는 타입이다.

조건부 타입을 작성할 때 주의사항은, 일반적인 삼항연산자처럼 조건에 부합하는 경우 즉시 리턴되므로, 좁은 범위의 타입부터 작성해야 정상적으로 타입을 추론할 수 있다는 것이다.

아래의 경우처럼, `DrinkBaseResponse`부터 조건문을 작성할 경우, 아래의 모든 타입이 `DrinkBaseResponse`를 확장하기 때문에, 모든 타입을 `CoffeeBaseResponse`로 추론하게 된다.

```typescript
type CoffeeResponseOf<T> = T extends DrinkBaseResponse
  ? CoffeeBaseResponse
  : T extends DrinkInfoResponse
  ? CoffeeInfoResponse
  : T extends DrinkDetailInfoResponse
  ? CoffeeDetailInfoResponse
  : never;

// CoffeeBaseResponse
type CoffeeBase = CoffeeResponseOf<DrinkBaseResponse>;
// CoffeeBaseResponse
type CoffeeInfo = CoffeeResponseOf<DrinkInfoResponse>;
// CoffeeBaseResponse
type CoffeeDetail = CoffeeResponseOf<DrinkDetailInfoResponse>;
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwhAQnAZwgCUICAHdEI5AbwChlkwBPciALmQHIFNsI3ANz0AvvXqhIsRCgxYcASRAx0pClRoQAHpBAATAmn458RdZWooGTclGBIuIAK4BbAEbQRTBHAWhOZBcPLzEJKWh4JGMFCAARCDA4YAAbZVULTRQdPUMYgXS1MksaG2Q+WNwIOBAuAjB7EABzEXFJcEjZZABBfTxCEmKsukZmNkDuOD7hMPbpKJReiELMq2QciAMjJbNBjTWyuwdA4M8ob2QCZya4KCc3M9bwjplopYSk1JWhtY2tnr6332pVGMCgzmAYDqDVALVmrHYyDijQA1rtVjQALz5UwDDEoAA+AP65h+RBECJQyNAKKBJRQ2PkBRURWBhOJdKyFPGSNRH2SaRZ+OQjJM8USAs5ayJ7wlXyFZIgInolJxe3pAHkYAAeAAqAD4RchdetdJs8tSQGi8YrRgB+NXo21MLgmv4W1FSoj2tVeiCjV2m3JGS0o-nyjLO5AOpk4cOCyNsgNBCAAN1C9AA9JnHTak6rYySGWr8VrtaGnWz9SJs7nSfmeYXCkbC6WdaG-dWsznC5X6SrG2L4y2xW3y3y5QnWfSu0A)

이를 사용해 인자의 조건에 따라 "커피 응답"을 찾을 수 있게 되었다.

그럼 이를 타입 가드 함수에 적용해볼 수 있을까?

"음료 기본 응답"을 확장하는 인자의 타입을 가지고, 인자의 조건에 맞는 "커피 응답"을 찾아서 인자가 조건에 부합하는 "커피 응답"임을 가드해주는 함수를 작성했다.

```typescript
function isCoffeeResponse<T extends DrinkBaseResponse>(
  response: T
): response is CoffeeResponseOf<T> {
  return response.type === 'coffee';
}
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwhAQnAZwgCUICAHdEI5AbwChlkwBPciALmQHIFNsI3ANz0AvvXqhIsRCgxYcASRAx0pClRoQAHpBAATAmn458RdZWooGTclGBIuIAK4BbAEbQRTBHAWhOZBcPLzEJKWh4JGMFCAARCDA4YAAbZVULTRQdPUMYgXS1MksaG2Q+WNwIOBAuAjB7EABzEXFJcEjZZABBfTxCEmKsukZmNkDuOD7hMPbpKJReiELMq2QciAMjJbNBjTWyuwdA4M8ob2QCZya4KCc3M9bwjplopYSk1JWhtY2tnr6332pVGMCgzmAYDqDVALVmrHYyDijQA1rtVjQALz5UwDDEoAA+AP65h+RBECJQyNAKKBJRQ2PkBRURWBhOJdKyFPGSNRH2SaRZ+OQjJM8USAs5ayJ7wlXyFZIgInolJxe3pAHkYAAeAAqAD4RchdetdJs8tSQCj+fKMorRgB+NU2wV2tmjLgmv4W1FSoiOtV+iAe42m3JGS1ovH2phOpm40nuphOCAAN1C9AA9Jm1ej7ar4ySGWr8VrtZG82z9SJs4GFe6C2LCkbC6WdZGg9WsznCy6gyqeb25SkW2K2+W+cPO8qYM4QAgwMAqMhgARW4q9WHzRHUZX6fqABSjKCKz30ACUXBPbJXRnXbLLBpGTBPYGcUBAyGv9IAdKrMQBPAVAIMyiEAA)

하지만, 이 함수는 에러가 발생한다.

```typescript
// A type predicate's type must be assignable to its parameter's type.
//   Type 'CoffeeResponseOf<T>' is not assignable to type 'T'.
//     'CoffeeResponseOf<T>' is assignable to the constraint of type 'T', but 'T' could be instantiated with a different subtype of constraint 'DrinkBaseResponse'.
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

> `isCoffeeInfoResponse`와 `isCoffeeDetailInfoResponse`는 함수 시그니쳐만 다를 뿐, 함수의 기능은 같다.

**"함수 기능은 같은데 시그니쳐만 다르다"**는 것이 문제의 원인이었다. 사실 이를 위한 타입스크립트의 기능은 [함수 오버로드](https://www.typescriptlang.org/docs/handbook/2/functions.html#function-overloads)이다.

<!-- prettier-ignore-start -->
```typescript
function isCoffeeResponse(response: DrinkDetailInfoResponse): response is CoffeeDetailInfoResponse;
function isCoffeeResponse(response: DrinkInfoResponse): response is CoffeeInfoResponse;
function isCoffeeResponse(response: DrinkBaseResponse): response is CoffeeBaseResponse {
  return response.type === 'coffee';
}
```
<!-- prettier-ignore-end -->

오버로드 함수는 [오버로드 시그니쳐와 구현 시그니쳐](https://www.typescriptlang.org/docs/handbook/2/functions.html#overload-signatures-and-the-implementation-signature)로 구성된다.

자바스크립트에서 오버로드는 인자의 조건(타입과 갯수)에 따른 분기를 함수 내부에 작성하는 방법이기 때문에, 타입스크립트에서도 오버로드 함수는 모든 오버로드 시그니쳐를 커버할 수 있는 하나의 구현 시그니쳐를 작성해야 한다.

구현 시그니쳐는 가장 아래에 위치하고, 나머지 오버로드 함수 시그니쳐와 호환되어야 한다.

따라서 `isCoffeeResponse`의 구현 시그니쳐에는 "음료 응답"의 가장 넓은 범위의 타입인 `DrinkBaseResponse`를 인자의 타입으로 갖고, "커피 응답"의 가장 넓은 범위의 타입인 `CoffeeBaseResponse`를 술어 부분의 추론 타입으로 작성했다.

그리고 나머지 두 오버로드 시그니쳐의 인자 타입인 `DrinkInfoResponse`과 `DrinkDetailInfoResponse`는 `DrinkBaseResponse`에 호환되고 술어 부분의 추론 타입인 `CoffeeInfoResponse`과 `CoffeeDetailInfoResponse`는 `CoffeeBaseResponse`에 호환된다.

```typescript
function getCaffeine(response: DrinkInfoResponse): number {
  if (isCoffeeResponse(response)) {
    // (parameter) response: CoffeeInfoResponse
    return response.caffeine;
  }

  return 0;
}

function getCoffeeBean(response: DrinkDetailInfoResponse): string | null {
  if (isCoffeeResponse(response)) {
    // (parameter) response: CoffeeDetailInfoResponse
    return response.coffeeBean;
  }

  return null;
}
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwhAQnAZwgCUICAHdEI5AbwChlkwBPciALmQHIFNsI3ANz0AvvXqhIsRCgxYcASRAx0pClRoQAHpBAATAmn458RdZWooGTclGBIuIAK4BbAEbQRTBHAWhOZBcPLzEJKWh4JGMFCAARCDA4YAAbZVULTRQdPUMYgXS1MksaG2Q+WNwIOBAuAjB7EABzEXFJcEjZZABBfTxCEmKsukZmNkDuOD7hMPbpKJReiELMq2QciAMjJbNBjTWyuwdA4M8ob2QCZya4KCc3M9bwjplopYSk1JWhtY2tnr6332pVGMCgzmAYDqDVALVmrHYyDijQA1rtVjQALz5UwDDEoAA+AP65h+RBECJQyNAKKBJRQ2PkBRURWBhOJdKyFPGSNRH2SaRZ+OQjJM8USAs5ayJ7wlXyFZIgInoMGcIAQYGAVGQwAITJw+IAFFBFVxqSAUfz5RlFQBKLgmtk6oz68WfQU2tkiVXqzXa3Wuo2O+lm1FSoj25DB4a6nHLBVelVqjVakDOwOK42m3k09F2h2K51xvNOsomsDOKBp6NWAB0lJFmOxvDFMzaPpT2qaiVQfmwASzbNDNPDEEjp2gIyYwBgyENAbFQbttqnTGQAHp13PyLc4K5EtAVzWiFxXaPRkxy5Xq4ra75-CAlaM2pfEtfkAAGJ5J32p5DdsBXSqGpBxDHMLStD1WXpSN6kaJpkCJFwUhSVcZznBdYiXNlbRXMomE3bdd33aQj2zV1IPPNcozfKsaLZO8xWAkALhfGiKzo5CUlaIA)

이제 하나의 함수 `isCoffeeResponse` 만으로, 타입 인자를 명시적으로 전달하지 않고 타입스크립트가 전달 받는 인자의 타입으로 추론할 수 있게 되었다.

오버로드 함수는 컴파일되면 하나의 함수만 남기 때문에, 기존에 같은 기능을 하는 함수가 여러 개 존재하는 것보다 번들사이즈를 줄일 수 있다.

그리고 같은 기능의 함수가 여러 개 있는 것보다 유지보수하기 쉬워진다.

### 함수 오버로딩에서의 유의사항

함수 오버로딩에서 [오버로드 시그니쳐의 순서는 중요](https://github.com/microsoft/TypeScript/issues/1860#issuecomment-72154737)하다.

적용 가능한 첫 번째 오버로드 시그니쳐가 선택되기 때문에, 조건부 타입을 작성할 때 처럼, 보다 구체적인 서명을 먼저 배치해야 한다.

그리고 `Array.filter`에서 오버로드 함수 자체가 인자로 사용될 때는 올바른 오버로드 시그니쳐를 추론하지 못하는 문제가 있었다.

<!-- prettier-ignore-start -->
```typescript
// 시그니쳐 (1)
function isCoffeeResponse(response: DrinkDetailInfoResponse): response is CoffeeDetailInfoResponse;
// 시그니쳐 (2)
function isCoffeeResponse(response: DrinkInfoResponse): response is CoffeeInfoResponse;
function isCoffeeResponse(response: DrinkBaseResponse): response is CoffeeBaseResponse {
  return response.type === 'coffee';
}

declare const drinkInfoResponses: DrinkInfoResponse[]
// 시그니쳐 (1)이 뒤에 올 때 에러가 발생함.
drinkInfoResponses.filter(isCoffeeResponse).map((response) => response.caffeine)

declare const drinkDetailInfoResponses: DrinkDetailInfoResponse[]
// 시그니쳐 (2)가 뒤에 올 때 에러가 발생함.
drinkDetailInfoResponses.filter(isCoffeeResponse).map((response) => response.coffeeBean)
```
<!-- prettier-ignore-end -->

> `시그니쳐 (1)`과 `시그니쳐 (2)`의 순서가 바뀔 때마다, 에러의 위치가 달라진다.

이런 케이스에서는 올바른 유형을 추론하기 위해 타입스크립트 컴파일러의 추론에 의존할 수 없는 경우이므로, `Array.filter`에 명시적으로 타입 인자를 넘겨주는 것으로 사용할 수 있다.

```typescript
declare const drinkInfoResponses: DrinkInfoResponse[];
drinkInfoResponses
  .filter<CoffeeInfoResponse>(isCoffeeResponse)
  .map((response) => response.caffeine);

declare const drinkDetailInfoResponses: DrinkDetailInfoResponse[];
drinkDetailInfoResponses
  .filter<CoffeeDetailInfoResponse>(isCoffeeResponse)
  .map((response) => response.coffeeBean);
```

[Playground Link](https://www.typescriptlang.org/play?ts=4.4.2#code/JYOwLgpgTgZghgYwgAgMIHsYwhAQnAZwgCUICAHdEI5AbwChlkwBPciALmQHIFNsI3ANz0AvvXqhIsRCgxYcASRAx0pClRoQAHpBAATAmn458RdZWooGTclGBIuIAK4BbAEbQRTBHAWhOZBcPLzEJKWh4JGMFCAARCDA4YAAbZVULTRQdPUMYgXS1MksaG2Q+WNwIOBAuAjB7EABzEXFJcEjZZABBfTxCEmKsukZmNkDuOD7hMPbpKJReiELMq2QciAMjJbNBjTWyuwdA4M8ob2QCZya4KCc3M9bwjplopYSk1JWhtY2tnr6332pVGMCgzmAYDqDVALVmrHYyDijQA1rtVjQALz5UwDDEoAA+AP65h+RBECJQyNAKKBJRQ2PkBRURWBhOJdKyFPGSNRH2SaRZ+OQjJM8USAs5ayJ7wlXyFZIgInoAHoVchADtDgA-awATTYAFmeQAAoAIwASnoMGcIAQYGAVGQwAITJw+MNUEVXGpIBR-PlGUVpq47rZDqMzvFn0F-rZIjVmt1BsNACZzZbrbb7Y7w67g-TPaipURA8hc8NHTjlgqYxarTa7SBQ9nFW6PbyaeiA0HFaGKx2Q2V3WBnFAG6WrAA6SkizHY3himZtPoIFK3FB8ahgZD6AtV+kEfM0wsQADaAF1VertfqjWbAC7jyEAJS2ABdHkIAaMeQgBlW5BPwA37YAAGuQQAcHsAXYHAAtV8d6G3Q9dyyAhxxgVJpENLMxXxU1x1cOByENFs2VNEUAD4S0VcdfH8EAIHNSCIGXVdyk0TcoO9X0o1ZPcD2YuVWPxM8L3ja9k1NADnzfT9v3-ICwIgpifS4o84IQlIkJQ2I0IwrCcLHItCOItlSLFKoaiouNABIxwAQnsAHQ7AB2W-i9UAH07kEAEN7ABrOwAI1cAEXGxN-STAA1VwAByeQQApUcAGXGILTOtMydMUj1wvM229I9iy0lBy3DI8RiYQdh1HEipxnWcKgEBcJBk+T4MQ6BkKi2JEvU7DYqyfDMSI5LSL8bAAio8KMwbFSBBYmLko42TI0SrsQ1SsUBpgg5RiykddPpSceXynhCpwYrIL5OSZqIBSKqgKrw2m6N6XQzD6uSpqWpI9a8GqEBjPVQBQro1QBACeQQABhcAUPHkEAD3HAATx5BABAJwAbpq26DTtg0ZyqU6AAB40t2iACKO1CAxhi7NIDHTWrIjqKNNZUZJOtjoaYWHpERqadqhqxUb6l0MYprGGqsa7FqyfTKgeomgA)

## 참고자료

- https://www.typescriptlang.org/docs/handbook/2/narrowing.html
- https://www.typescriptlang.org/ko/docs/handbook/2/generics.html
- https://www.typescriptlang.org/docs/handbook/2/conditional-types.html
- https://www.typescriptlang.org/docs/handbook/2/functions.html#function-overloads
