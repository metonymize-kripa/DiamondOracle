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
	  {
    title: 'How does the 💎 Oracle make such precise estimates? Smells like old fish tacos.',
    slug: 'how-it-works',
    html: `
			<p>It's called RND. Not being rando, it's not random -- it stands for Risk Neutral Distribution. It is basically ... </p>
<p> You can read a bit more here: <a href='https://www.globalcapital.com/article/k6543wh6f19l/option-prices-imply-a-probability-distribution'> Gentle introduction </a> </p>
		`,
  },
];

posts.forEach(post => {
  post.html = post.html.replace(/^\t{3}/gm, '');
});

export default posts;
