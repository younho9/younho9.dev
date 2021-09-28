---
hero: ./images/2021-09-28-sharing-prettier-config-1.png
slug: 'sharing-prettier-config'
title: '프리티어(Prettier) 설정 공유하기'
date: 2021-09-28
tags: ['Prettier']
author: younho9
excerpt: 개인 프로젝트의 프리티어 설정을 일관되게 유지하자.
---

## TL;DR

- 프로젝트마다 프리티어 설정 파일을 개별적으로 만들다보면, 일관되게 관리하기 어려울 수 있다.
- 설정 파일을 따로 만들어 배포하고 관리하자.
- JSDoc을 사용하면 타입 지원을 받을 수 있다.

## Intro

JS 생태계는 수많은 툴들이 있고, 개발자마다 선호하는, 또는 프로젝트에 적합한 툴들이 다양하지만, 프리티어는 설정이 간단하면서도 생산성에 큰 도움이 되기 때문에 많이 사용되고 있는 것 같다.

특히, 개인이 선호하는 설정이나 팀에서 협의한 설정으로 코드 스타일을 일관되게 관리할 수 있다는 점이 큰 장점이다.

그런데 프리티어 설정 파일을 프로젝트마다 개별적으로 생성한다면 어떤 이유로 인해 한 프로젝트에서 설정을 바꾸게 되었을 때 일관성이 깨지거나, 많은 프로젝트들의 설정을 변경하는 번거로운 작업을 하게 될 수 있다.

## 설정 파일 공유하기

이를 위해서 프리티어는 [설정 파일을 쉽게 공유할 수 있는 방법](https://prettier.io/docs/en/configuration.html#sharing-configurations)을 제공한다.

바로 `package.json`의 `prettier` 필드에 사용할 프리티어 설정 패키지의 이름을 명시하는 것이다.

```json
{
  "name": "my-cool-library",
  "version": "9000.0.1",
  "prettier": "@company/prettier-config",
  "devDependencies": {
    "@company/prettier-config": "1.0.0"
  }
}
```

이렇게 하면, 별도의 프리티어 설정 파일을 프로젝트에 생성하거나 `package.json`에 명시하지 않고도, 패키지에 명시한 프리티어 룰을 적용할 수 있게 된다.

## 프리티어 설정 패키지 만들기

공유할 프리티어 설정 패키지를 만들기 위해 패키지를 생성한다.

`npm init -y`로 `package.json`을 생성하고 패키지에 관한 정보를 기입한다.

```json
// package.json
{
  "name": "@username/prettier-config",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "keywords": [],
  "author": "username",
  "license": "ISC",
  "main": "src/index.js",
  "files": ["src"],
  "dependencies": {
    "@types/prettier": "2.4.1"
  },
  "devDependencies": {
    "prettier": "2.4.0"
  },
  "peerDependencies": {
    "prettier": "*"
  },
  "publishConfig": {
    "access": "public"
  }
}
```

> 각 필드에 대한 자세한 설명은 [npm 공식 문서](https://docs.npmjs.com/cli/v7/configuring-npm/package-json)를 참고

`@username/prettier-config` 처럼 [스코프를 가진 패키지 이름](https://docs.npmjs.com/cli/v7/using-npm/scope)을 사용한다면, public으로 배포하기 위해 `publishConfig: { "access": "public" }`을 추가해준다.

그리고 `main` 필드에 등록한 `index.js` 파일에 프리티어 설정 객체(configuration object)를 export 해준다.

```js
// index.js
/** @type {import('prettier').Options} */
module.exports = {
  printWidth: 80,
  tabWidth: 2,
  useTabs: false,
  semi: true,
  singleQuote: true,
};
```

위의 `package.json`에서 의존성으로 `@types/prettier`를 추가해 주었는데, 이 패키지가 제공하는 프리티어 설정 타입(`Options`)을 JSDoc으로 명시해주면 타입 지원을 받을 수 있어서, 옵션의 역할이 헷갈릴 때, 문서를 찾지 않아도 힌트를 얻을 수 있다.

<div class="Image__Small">
  <img
    src="./images/2021-09-28-sharing-prettier-config-2.png"
    alt="JSDoc을 통한 타입 지원"
  />
  <figcaption>JSDoc을 통한 타입 지원</figcaption>
</div>

이렇게 구성한 패키지를 [`npm publish`](https://docs.npmjs.com/cli/v7/commands/npm-publish) 명령어로 배포한다.

이후 프리티어 설정을 적용할 프로젝트에서 패키지를 설치하고 위에 언급한 방법으로 `package.json`에 명시한다.

```bash
npm install -D @username/prettier-config
```

이렇게 하면, 프로젝트마다 개별 프리티어 설정 파일을 관리하는 것이 아니라, 패키지의 버전으로 관리할 수 있게 되기 때문에, 프로젝트에서 의존성 버전을 업데이트하면서 자연스럽게 프리티어 설정을 일관되게 적용하게 된다.

또한, 커밋 메시지를 잘 작성해두면, 특정 옵션에 대한 변경이 왜 필요했는지 맥락을 한 곳에서 관리하게 되기 때문에, 본인에게 도움이 될 뿐만 아니라, 팀끼리 공유할 때에도 도움이 될 수 있다.

## 예시

https://github.com/younho9/lib/tree/main/packages/prettier-config

## 참고자료

- https://prettier.io/docs/en/configuration.html#sharing-configurations
