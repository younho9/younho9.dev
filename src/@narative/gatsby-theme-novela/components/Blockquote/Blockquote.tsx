import styled from '@emotion/styled';
import mediaqueries from '@styles/media';

const Blockquote = styled.blockquote`
  transition: ${(p) => p.theme.colorModeTransition};
  margin: 20px auto 30px;
  color: ${(p) => p.theme.colors.articleText};
  font-family: ${(p) => p.theme.fonts.serif};

  ${mediaqueries.tablet`
    margin: 20px auto 30px;
  `};

  & > p {
    font-family: ${(p) => p.theme.fonts.serif};
    max-width: 680px !important;
    padding-bottom: 0;
    color: ${(p) => p.theme.colors.grey};
    width: 100%;
    margin: 0 auto;
    font-size: 24px;
    line-height: 1.32;
    font-weight: bold;

    ${mediaqueries.tablet`
      font-size: 25px;
      max-width: 486px !important;
    `};

    ${mediaqueries.phablet`
      font-size: 20px;
      padding: 0 20px 0 40px;
    `};
  }
`;

export default Blockquote;
