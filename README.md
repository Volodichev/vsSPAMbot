# vsspambot
Antispam moderator bot for telegram chats

_*Make sure @vsspambot is an admin._

--------------------------------------------

_/help_ — show info and commands

_/language_ — change language

_/no_link_ - forbid links

_/no_repost_ — forbid reposts

_/no_uname_ — forbid usernames

_/no_email_ — forbid email

_/no_sticker_ — forbid stickers

_/no_doc_ — forbid documents

_/no_photo_ — forbid pictures

_/no_audio_ — forbid music

_/no_video_ — forbid video

_/no_vidnote_ — forbid video circles

_/no_gif_ — forbid animation

_/no_poll_ — forbid polls

_/no_voice_ — forbid voices

_/no_fword_ — forbid fwords

_/no_admins_ — only creator edit

_/no_captcha_ — don't ask newbies, is he a bot

_/quarantine_ — quarantine for newbies "quarantine 24"

_/settings_ — settings
        


###TODO:
- [x] add README
- [x] only admins or creator can edit settings
- [x] remove forwarded messages, links, usernames in newbies posts for first 24(N) hours [like @daysandbox_bot]
- [x] remove messages type: link, sticker, gif, voice attachment, file attachment and other  [like @watchdog_robot, @nosticker_bot]
- [x] restrict newbies rights while solve captcha button [like https://tgdev.io/bot/orgrobot И https://github.com/F0rzend/antirobot_aiogram]
- [x] /no_captcha
- [x] add throttling
- [x] new test bot
- [x] приветствие с инструкцией, если добавили как участника и если добавилил как админа
- [ ] put github
- [ ] move to restapi
- [ ] add ubuntu - redis



####later:
- [ ] add tests
- [ ] clean requirements
- [ ] add /readonly
- [ ] forbid spam languages No China Bot removes CJK spam messages from your chat [like @nochinabot, @noarab_bot] + не показывать настройку /no_arabic для арабских языков, /no_chineeze для китайских
- [ ] add check for street address  ex.: Адрес: Римского-Корсакова, д. 11, корп. 8. 
- [ ] remove custom list words [like @nopigrobot, @grep_robot] 
- [ ] hide info about entrance of new user [like @joinhider_bot]
- [ ] limit of message in day/hour/min [like @freqrobot]
- [ ] cmd /reset to default chat settings
- [ ] записывать всех пользователей в общую db for all users
- [ ] add statistics
- [ ] удалять старые посты