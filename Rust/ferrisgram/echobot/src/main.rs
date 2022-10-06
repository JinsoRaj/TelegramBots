use ferrisgram::error::{GroupIteration, Result};
use ferrisgram::ext::filters::message;
use ferrisgram::ext::handlers::{CommandHandler, MessageHandler};
use ferrisgram::ext::{Context, Dispatcher, Updater};
use ferrisgram::Bot;

#[allow(unused)]
#[tokio::main]

async fn main() {
    // This function creates a new bot instance and the error is handled accordingly
    let bot = match Bot::new("Bot Token Here", None).await {
        Ok(bot) => bot,
        Err(error) => panic!("failed to create bot: {}", &error),
    };

    let mut dispatcher = &mut Dispatcher::new(&bot);

    dispatcher.add_handler(CommandHandler::new("start", start));
    dispatcher.add_handler_to_group(
        MessageHandler::new(
            echo,
            message::Text::filter().or(message::Caption::filter()),
        ),
        1,
    );

    let mut updater = Updater::new(&bot, dispatcher);

    updater.start_polling(true).await;
}


async fn start(bot: Bot, ctx: Context) -> Result<GroupIteration> {
    let msg = ctx.effective_message.unwrap();
    msg.reply(
        &bot,
        "Hey! I am an echo bot built using [Ferrisgram](https://github.com/ferrisgram/ferrisgram).
I will repeat your messages.",
    )
    .parse_mode("markdown".to_string())
    .disable_web_page_preview(true)
    .send()
    .await?;
    Ok(GroupIteration::EndGroups)
}

async fn echo(bot: Bot, ctx: Context) -> Result<GroupIteration> {
    let chat = ctx.effective_chat.unwrap();
    let msg = ctx.effective_message.unwrap();
    bot.copy_message(chat.id, chat.id, msg.message_id)
        .send()
        .await?;
    Ok(GroupIteration::EndGroups)
}