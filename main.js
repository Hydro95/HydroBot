var Discord = require('discord.js');

var bot = new Discord.Client();

var prefix = '=';

bot.on('message', msg => {
    if (msg.author.bot) {
        return;
    }

    if (msg.content.startsWith(prefix)) {
        var input = msg.content.substring(1);

        console.log('Received Command: ' + input);


    }

});

bot.on('ready', () => {
    console.log('Hey look, I\'m alive!');
});

bot.on('disconnect', () => {
    console.log('Goodbye!');
    bot.user.setStatus('offline');
});

bot.login(LOGIN_TOKEN);
