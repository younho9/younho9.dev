/**
 * This react helmt code is adapted from
 * https://themeteorchef.com/tutorials/reusable-seo-with-react-helmet.
 *
 * A great tutorial explaining how to setup a robust version of an
 * SEO friendly react-helmet instance.
 *
 *
 * Use the Helmt on pages to generate SEO and meta content!
 *
 * Usage:
 * <SEO
 *   title={title}
 *   description={description}
 *   image={image}
 * />
 *
 */

import React from 'react';
import Helmet from 'react-helmet';
import {graphql, useStaticQuery} from 'gatsby';

interface HelmetProps {
  title: string;
  description?: string;
  pathname: string;
  image?: string;
  url?: string;
  canonicalUrl?: string;
  published?: string;
  timeToRead?: string;
}

const seoQuery = graphql`
  {
    allSite {
      edges {
        node {
          siteMetadata {
            description
            social {
              url
              name
            }
            siteUrl
            title
          }
        }
      }
    }
  }
`;

const themeUIDarkModeWorkaroundScript = [
  {
    type: 'text/javascript',
    innerHTML: `
    (function() {
      try {
        var mode = localStorage.getItem('theme-ui-color-mode');
        if (!mode) {
          localStorage.setItem('theme-ui-color-mode', 'light');
        }
      } catch (e) {}
    })();
  `,
  },
];

const SEO: React.FC<HelmetProps> = ({
  title,
  description,
  children,
  pathname,
  image,
  published,
  timeToRead,
  canonicalUrl,
}) => {
  const results = useStaticQuery(seoQuery);
  const site = results.allSite.edges[0].node.siteMetadata;
  const twitter = site.social.find((option) => option.name === 'twitter') || {};

  const fullURL = (path: string) =>
    path ? `${site.siteUrl}${path}` : site.siteUrl;

  // If no image is provided lets looks for a default novela static image
  image = image ? image : fullURL('/preview.png');

  const metaTags = [
    {charset: 'utf-8'},
    {
      'http-equiv': 'X-UA-Compatible',
      'content': 'IE=edge',
    },
    {
      name: 'viewport',
      content: 'width=device-width, initial-scale=1',
    },
    {
      name: 'theme-color',
      content: '#fff',
    },
    {itemprop: 'name', content: title || site.title},
    {itemprop: 'description', content: description || site.description},
    {itemprop: 'image', content: image},
    {name: 'description', content: description || site.description},

    {name: 'twitter:card', content: 'summary_large_image'},
    {name: 'twitter:site', content: site.name},
    {name: 'twitter:title', content: title || site.title},
    {name: 'twitter:description', content: description || site.description},
    {name: 'twitter:creator', content: twitter.url},
    {
      name: 'twitter:image',
      content: image,
    },

    {property: 'og:title', content: title || site.title},
    {property: 'og:url', content: site.siteUrl + pathname},
    {property: 'og:image', content: image},
    {property: 'og:description', content: description || site.description},
    {property: 'og:site_name', content: site.title},
    {property: 'og:type', content: 'website'},
  ];

  if (published) {
    metaTags.push({name: 'article:published_time', content: published});
  }

  if (timeToRead) {
    metaTags.push({name: 'twitter:label1', value: 'Reading time'});
    metaTags.push({name: 'twitter:data1', value: `${timeToRead} min read`});
  }

  return (
    <Helmet
      title={title || site.title}
      htmlAttributes={{lang: 'en'}}
      script={themeUIDarkModeWorkaroundScript}
      meta={metaTags}
    >
      {canonicalUrl && <link rel="canonical" href={canonicalUrl} />}
      {children}
    </Helmet>
  );
};

export default SEO;
