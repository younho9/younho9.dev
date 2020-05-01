module.exports = {
  siteMetadata: {
    title: `younho9.dev`,
    name: `younho9`,
    siteUrl: `https://younho9.dev`,
    description: `younho9의 기술 블로그, 웹 프론트엔드 개발 일지, 느려도 꾸준하게`,
    hero: {
      heading: `💪 Hello. I'm younho9, <br> studying Web Development`,
      maxWidth: 652,
    },
    social: [
      {
        name: `github`,
        url: `https://github.com/younho9`,
      },
      {
        name: `instagram`,
        url: `https://www.instagram.com/younho_9/`,
      }
    ],
  },
  plugins: [
    {
      resolve: "@narative/gatsby-theme-novela",
      options: {
        contentPosts: "content/posts",
        contentAuthors: "content/authors",
        basePath: "/",
        authorsPage: true,
        sources: {
          local: true,
          // contentful: true,
        },
      },
    },
    {
      resolve: `gatsby-plugin-manifest`,
      options: {
        name: `younho9.dev`,
        short_name: `younho9.dev`,
        start_url: `/`,
        background_color: `#fff`,
        theme_color: `#fff`,
        display: `standalone`,
        icon: `src/assets/favicon.png`,
      },
    },
    {
      resolve: `gatsby-plugin-netlify-cms`,
      options: {
      },
    },
    {
      resolve: `gatsby-plugin-google-analytics`,
      options: {
        trackingId: `UA-159972507-2`,
      }
    },
    `gatsby-plugin-offline`
  ],
};
