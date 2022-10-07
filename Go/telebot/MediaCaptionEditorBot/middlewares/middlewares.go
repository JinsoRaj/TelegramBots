package middlewares

import (
	"MediaCaptionEditorBot/state"

	"golang.org/x/exp/slices"
	tele "gopkg.in/telebot.v3"
)

func MiddlewareAuthorizedGroup(next tele.HandlerFunc) tele.HandlerFunc {
	config := state.State.Config

	return func(c tele.Context) error {
		chat := c.Chat()

		if chat == nil || !slices.Contains(config.Telegram.AuthorizedChats, chat.ID) {
			return nil
		}

		return next(c)
	}
}
