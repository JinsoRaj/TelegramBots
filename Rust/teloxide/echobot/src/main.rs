use teloxide::prelude::*;

#[tokio::main]
async fn main() {
    pretty_env_logger::init();
    log::info!("Starting the echo bot...");

    let bot = Bot::from_env();

    teloxide::repl(bot, |bot: Bot, msg: Message| async move {
        let text = msg.text().unwrap_or("");
        if !text.is_empty() {
            bot.send_message(msg.chat.id, text).await?;
        }
        Ok(())
    })
    .await;
}
