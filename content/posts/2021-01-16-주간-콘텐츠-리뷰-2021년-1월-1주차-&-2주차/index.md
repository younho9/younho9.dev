---
title: 주간 콘텐츠 리뷰 - 2021년 1월 1주차 & 2주차
author: younho9
date: 2021-01-16
hero: ./images/hero.jpeg
slug: 2021-01-1-and-2
excerpt: 깃헙, 페이스북, 트위터, 유튜브, 미디움 등에서 매일마다 흥미로운 콘텐츠를 소비하고 있다. 하지만 콘텐츠에서 소개하는 기술을 실제로 적용하거나, 인사이트를 얻어내기 위해서는 단순히 소비하는 것에서 그치지 않고, 스스로 생각하는 시간이 필요한 것 같다.
---

깃헙, 페이스북, 트위터, 유튜브, 미디움 등에서 매일마다 흥미로운 콘텐츠를 소비하고 있다. 하지만 콘텐츠에서 소개하는 기술을 실제로 적용하거나, 인사이트를 얻어내기 위해서는 단순히 소비하는 것에서 그치지 않고, 스스로 생각하는 시간이 필요한 것 같다.

그래서 앞으로는 한 주간 흥미로웠던 깃헙 프로젝트나 블로그 글, 유튜브 콘텐츠 그리고 도움을 얻었던 깃헙이나 스택오버플로우 답변, 공식 문서 내용 등을 기억해볼겸 정리하려고 한다. 그리고 새로 사용해본 도구나 노트 기록들도 같이 정리해봤다.

## 읽기 목록

- [Notes on TypeScript: Phantom Types](https://dev.to/busypeoples/notes-on-typescript-phantom-types-kg9) : "어떻게 하면 RGB hex value( `#ffffff` ) 같은 특정 형태의 문자열을 타이핑할 수 있을까"하는 고민으로 검색하면서 찾은 키워드 "팬텀 타입"에 대한 글이다. 아직 내용을 다 이해하지 못했고, 이를 적용하기에는 해결하려는 문제보다 과잉이라고 판단해서 스킵했지만, 나중에라도 팬텀 타입에 대해 알아보기 위해 북마크해두었다.

- [8-Digit Hex Codes?](https://css-tricks.com/8-digit-hex-codes/) : Hex 코드로 Opacity를 지정하는 방법을 소개한다.

- [Jest - toThrowError](https://jestjs.io/docs/en/expect#tothrowerror) : Jest에서 에러를 expect하는 방법.

- [Keeping your CSS in JS clean](https://medium.com/swlh/keeping-your-css-in-js-clean-with-stylelint-8822c8c1543a) : CSS in JS에 Stylelint를 적용하는 방법을 소개한다. 최근 eslint의 장점을 느끼기 시작해서 Stylelint도 한번 적용해봐야겠다.

- [아하 REST API 서버 개발 (1~14)](https://medium.com/aha-official/%EC%95%84%ED%95%98-rest-api-%EC%84%9C%EB%B2%84-%EA%B0%9C%EB%B0%9C-1-90b5da9e6593) : ExpressJS + Sequelize + JWT 스택으로 유저 인증 REST API 서버를 구축하는 Step by Step 튜토리얼. 각 스텝 별로 구현하는 방법 뿐만 아니라, 이유를 자세히 설명하는 방식으로 진행되는 점이 좋았다. 유저 인증 방식이나, Redis 캐싱 방법, ExpressJS에서 백엔드 구조를 잡는 방법을 이유와 함께 이해할 수 있어서 도움을 많이 얻었다. 강추.

## Github

- [React + TypeScript Cheatsheets](https://github.com/typescript-cheatsheets/react) : 리액트 + 타입스크립트의 치트시트다. TS로 리액트 코드를 작성하면서 생기는 몇 가지 고민들(JSX.Element vs React.ReactNode, type vs interface, Why `React.FC` discouraged?)에 대한 짧은 답을 설명하고, Hokks, Context, defaultProps 등을 사용할 때의 패턴을 소개한다. 그외에도 추천하는 코드베이스나 유용한 커스텀 훅도 링크되어 있어서 앞으로 자주 참조하면 React + TS 기술 스택에 더 익숙해지는데 도움이 될 것 같다.

- [Change Case Extension for Visual Studio Code](https://github.com/wmaurer/vscode-change-case) : VSCode에서 케이스를 변환해주는 익스텐션

- [Sort Package.json](https://github.com/keithamus/sort-package-json) : package.json 수정할 때 순서를 어떻게 해야되나 고민했었는데, husky로 커밋 훅에 달아두니 고민하지 않아도 되서 편했다. 순서는 [package.json](https://docs.npmjs.com/cli/v6/configuring-npm/package-json) 문서를 참조하고, 좋은(?) 항목을 추가했다고 설명한다.

- [eslint-plugin-import](https://github.com/benmosher/eslint-plugin-import) : import와 관련된 린트 규칙을 제공한다. 특히 `import/order` 규칙은 import의 순서를 린트해주는데, 평소 import 순서가 뒤죽박죽이면 괜히 지저분해보이고, 그걸 또 수정하자니 번거로웠는데 매우 편리했다.

- [Under the hood: React](https://github.com/Bogdan-Lyashenko/Under-the-hood-ReactJS) : 아직 읽진 않았지만, 리액트 내부 원리를 깊이 뜯어볼 수 있고, 한국어 번역도 있어서 나중에 꼭 읽으려고 스타를 눌렀다.

## Youtube

- [Next Level Github Profile README](https://www.youtube.com/watch?v=ECuqb5Tv9qI&t=630s) : 깃헙 프로필을 꾸미고 관리하는 방법 소개. 최근 작성 블로그 글 목록을 Github Action으로 구현하는 부분이 설명되어 있다.

- [velopert님의 Live Coding Season 3](https://www.youtube.com/playlist?list=PL9FpF_z-xR_EADAJcF3xrFftyD41mg1ak) : 벨로퍼트님의 주식 관련 신규 프로젝트 라이브 코딩. 벨로퍼트님이 개발하면서 생각하시는 것들이나 개발일지를 작성하는 습관 등을 라이브로 보면서 배울 수 있어서 좋다.

## Websites

- [Product Hunt - Web App](https://www.producthunt.com/topics/web-app) : 웹 앱 프로덕트들을 소개해준다. 최신 웹 앱 트렌드를 파악하거나 유용한 도구들을 발견할 수 있다.  

- [Custom Shape Dividers](https://www.shapedivider.app/) : 랜딩페이지에 넣을만한 웨이브 svg를 생성해준다.

- [mobbin](https://mobbin.design/) : 여러 앱의 UI를 한 눈에 볼 수 있다.

- [2020 State of JS](https://2020.stateofjs.com/ko-KR/) & [2020 State of CSS](https://2020.stateofcss.com/en-US/report/) : JS와 CSS의 연말 축제와 시상식. 확실히 프론트엔드의 트렌드가 정말 빠르게 바뀌고 있다는 것과 신기술이 쏟아져 나온다는 것을 느낄 수 있었다.

- [designcode](https://designcode.io/) : 디자인과 코드. 화려한 UI를 가진 디자인 및 개발 강의 사이트. (유료)

- [kentcodds.com](https://kentcdodds.com/blog/) : 2020 State of JS 를 통해 알게 되었다. 이분이 React Guru 인가..?

- [rw;eruch](https://www.robinwieruch.de/) : 2020 State of JS 를 통해 알게 되었다. 이분이 React Guru 인가..? 2

## Tools

- [everyday](https://everyday.app/) : 습관 추적 앱. 무료 버전은 3개의 습관을 등록할 수 있다. 깃헙 잔디 같은 느낌으로 습관을 관리할 수 있다. 애플워치부터 아이폰, 아이패드, 데스크탑 앱, 웹사이트 버전까지 지원한다. 엄청 완성도가 있는 것은 아니지만 가장 간단하고 직관적으로 쓸 수 있어서 좋다.

- [Alfred](https://www.alfredapp.com/workflows/) : Spotlight만 쓰다가 최근에 Alfred를 사용했는데, 북마크 워크플로우 하나만으로도 사용 가치가 있는 것 같다. 그 외에도 VSCode, Bear, Notion Search, Daum Dictionary, Papago 등의 워크플로우를 상당히 잘 활용하고 있다.

## Notes

- [TypeScript + React + Storybook으로 디자인 시스템 구축하기](https://til.younho9.dev/log/2021/2021-01-01-210101)

- [Merge Options와 GitHub과 GitLab의 차이](https://til.younho9.dev/log/2021/2021-01-03-210103)

- [Crontab으로 매일 스크린샷 관리하기](https://til.younho9.dev/log/2021/2021-01-10-210110)

- [리눅스 폴더 권한 변경](https://til.younho9.dev/log/2021/2021-01-11-210111)

- [sudo: unable to resolve host 에러 해결](https://til.younho9.dev/log/2021/2021-01-13-210113)

- [ssh를 이용하여 원격 서버와 양방향 파일 전송하기](https://til.younho9.dev/log/2021/2021-01-15-210115)

