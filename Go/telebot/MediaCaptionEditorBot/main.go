package main

import (
	"log"
	"time"

	"MediaCaptionEditorBot/middlewares"
	"MediaCaptionEditorBot/state"

	tele "gopkg.in/telebot.v3"
)

func main() {
	config := state.State.Config
	config.LoadConfig()

	bot, err := tele.NewBot(tele.Settings{
		URL:    config.Telegram.ApiURL,
		Token:  config.Telegram.BotToken,
		Poller: &tele.LongPoller{Timeout: 10 * time.Second},
	})
	if err != nil {
		log.Fatalln("could not initialize bot : ", err)
	}
	log.Printf("Telegram bot logged in as @%s\n", bot.Me.Username)
	state.State.Bot = bot
	state.State.StartTime = time.Now()

	bot.Handle(tele.OnChannelPost, editCaption, middlewares.MiddlewareAuthorizedGroup)

	bot.Start()
}

func editCaption(c tele.Context) error {
	bot := c.Bot()
	msg := c.Update().ChannelPost
	if msg == nil || msg.Media() == nil || msg.IsForwarded() {
		return nil
	}

	mediaType := msg.Media().MediaType()
	if mediaType != "video" && mediaType != "document" {
		return nil
	}

	caption := msg.Caption
	var newCaption string
	newCaption += caption
	newCaption += `
This has been added by the bot
You can do multiline stuff as well
`

	_, err := bot.EditCaption(msg, newCaption, tele.ModeHTML)
	if err != nil {
		log.Println(err)
	}
	return err
}
