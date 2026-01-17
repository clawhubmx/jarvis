-- simple test hello command

local lang = jarvis.context.language
local hour = tonumber(jarvis.context.time.hour)

-- determine greeting based on time
local greeting
if hour >= 5 and hour < 12 then
    greeting = lang == "ru" and "Доброе утро" or "Good morning"
elseif hour >= 12 and hour < 17 then
    greeting = lang == "ru" and "Добрый день" or "Good afternoon"
elseif hour >= 17 and hour < 22 then
    greeting = lang == "ru" and "Добрый вечер" or "Good evening"
else
    greeting = lang == "ru" and "Доброй ночи" or "Good night"
end

jarvis.log("info", "Greeting user: " .. greeting)
jarvis.audio.play_reply()

return { chain = true }