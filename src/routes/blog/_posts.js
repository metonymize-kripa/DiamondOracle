// Ordinarily, you'd generate this data from markdown files in your
// repo, or fetch them from a database of some kind. But in order to
// avoid unnecessary dependencies in the starter template, and in the
// service of obviousness, we're just going to leave it here.

// This file is called `_posts.js` rather than `posts.js`, because
// we don't want to create an `/blog/posts` route — the leading
// underscore tells Sapper not to do that.

const posts = [
  {
    title: 'How can I get involved?',
    slug: 'how-can-i-get-involved',
    html: `
			<p>We're so glad you asked! Enter the <a href='https://github.com/metonymize-kripa/DiamondOracle'> matrix </a>. Everyone is welcome, especially you!</p>
		`,
  },
];

posts.forEach(post => {
  post.html = post.html.replace(/^\t{3}/gm, '');
});

export default posts;
