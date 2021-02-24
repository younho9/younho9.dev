import React, { useRef, useEffect } from 'react';
import { useColorMode } from 'theme-ui';

export interface IUtterancesProps {
  repo: string;
}

const utterancesSelector = 'iframe.utterances-frame';

const ArticleUtterances: React.FC<IUtterancesProps> = React.memo(({ repo }) => {
  const [colorMode] = useColorMode();
  const isDark = colorMode === `dark`;
  const utterancesTheme = isDark ? 'github-dark' : 'github-light';
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const utterancesEl = containerRef.current.querySelector(
      utterancesSelector
    ) as HTMLIFrameElement;

    const createUtterancesEl = () => {
      const script = document.createElement('script');

      script.src = 'https://utteranc.es/client.js';
      script.setAttribute('repo', repo);
      script.setAttribute('issue-term', 'pathname');
      script.setAttribute('label', 'comment');
      script.setAttribute('theme', utterancesTheme);
      script.crossOrigin = 'anonymous';
      script.async = true;

      containerRef.current.appendChild(script);
    };

    const postThemeMessage = () => {
      const message = {
        type: 'set-theme',
        theme: utterancesTheme,
      };

      utterancesEl.contentWindow.postMessage(message, 'https://utteranc.es');
    };

    utterancesEl ? postThemeMessage() : createUtterancesEl();
  }, [repo, utterancesTheme]);

  return <div ref={containerRef} />;
});

ArticleUtterances.displayName = 'Utterances';

export default ArticleUtterances;
