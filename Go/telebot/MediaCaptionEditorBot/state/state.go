package state

import (
	"time"

	"MediaCaptionEditorBot/config"

	tele "gopkg.in/telebot.v3"
	"gorm.io/gorm"
)

type state struct {
	Bot      *tele.Bot
	Config   *config.Config
	Database *gorm.DB

	StartTime time.Time
}

var State state

func init() {
	State.Config = &config.Config{}
}
