const { TwitterApi } = require('twitter-api-v2');

// Credenciais do .env
const client = new TwitterApi({
  appKey: process.env.TWITTER_CONSUMER_KEY,
  appSecret: process.env.TWITTER_CONSUMER_SECRET,
  accessToken: process.env.TWITTER_ACCESS_TOKEN,
  accessSecret: process.env.TWITTER_ACCESS_TOKEN_SECRET,
});

const tweet = process.argv[2] || 'Teste do @Jesussemfiltro 🙏';

async function postTweet() {
  try {
    // API v2
    const result = await client.v2.tweet(tweet);
    console.log('✅ Tweet postado com sucesso!');
    console.log('ID:', result.data.id);
    console.log('Texto:', result.data.text);
  } catch (error) {
    console.error('❌ Erro ao postar:', error.message);
    if (error.data) {
      console.error('Detalhes:', JSON.stringify(error.data, null, 2));
    }
  }
}

postTweet();
