package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
	"github.com/PaulSonOfLars/gotgbot/v2/ext/handlers"
)

func main() {

	botToken, present := os.LookupEnv("BOT_TOKEN")
	if botToken == "" || !present {
		panic("missing environment variable 'BOT_TOKEN'")
	}

	bot, err := gotgbot.NewBot(botToken, &gotgbot.BotOpts{
		Client: http.Client{},
		DefaultRequestOpts: &gotgbot.RequestOpts{
			Timeout: gotgbot.DefaultTimeout,
		},
	})
	if err != nil {
		panic("failed to initialize bot : " + err.Error())
	}

	updater := ext.NewUpdater(&ext.UpdaterOpts{
		ErrorLog: nil,
		DispatcherOpts: ext.DispatcherOpts{
			// If an error is returned by a handler, log it and continue going.
			Error: func(_ *gotgbot.Bot, _ *ext.Context, err error) ext.DispatcherAction {
				fmt.Println("an error occurred while handling update:", err.Error())
				return ext.DispatcherActionNoop
			},
			MaxRoutines: ext.DefaultMaxRoutines,
		},
	})

	dispatcher := updater.Dispatcher
	dispatcher.AddHandler(handlers.NewMessage(
		func(msg *gotgbot.Message) bool {
			return msg.Chat.Type == "private"
		},
		func(b *gotgbot.Bot, c *ext.Context) error {
			_, err := b.CopyMessage(
				c.EffectiveChat.Id,
				c.EffectiveChat.Id,
				c.EffectiveMessage.MessageId,
				&gotgbot.CopyMessageOpts{
					ReplyToMessageId:         c.EffectiveMessage.MessageId,
					AllowSendingWithoutReply: true,
				},
			)
			return err
		},
	))

	err = updater.StartPolling(bot, &ext.PollingOpts{
		DropPendingUpdates: true,
		GetUpdatesOpts: gotgbot.GetUpdatesOpts{
			Timeout: 9,
			RequestOpts: &gotgbot.RequestOpts{
				Timeout: time.Second * 10,
			},
		},
	})
	if err != nil {
		panic("failed to start polling : " + err.Error())
	}

	log.Printf(
		"Echo bot started as '%s' [ @%s ]\n",
		bot.FirstName,
		bot.Username,
	)

	updater.Idle()
}
