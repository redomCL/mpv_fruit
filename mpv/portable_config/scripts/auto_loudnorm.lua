--[[
-- 该实现和 https://github.com/mpv-player/mpv/issues/11541 问题一致

function check_achannels()
	local channel_count = mp.get_property_number("audio-params/channel-count")
	if channel_count and channel_count > 2 then
		mp.commandv("af", "pre", "@vocal:loudnorm")
	else
		mp.commandv("af", "remove", "@vocal")
	end
end

mp.observe_property("audio-params/channel-count", "number", check_achannels)

]]


-- 改用此版本可按预期工作

function check_achannels(prop, value)
	if prop == "path" or prop == "aid" then
		local achannels = mp.get_property_number("audio-params/channel-count", 0)
		--print("achannels " .. achannels)
		if achannels > 2 then
			mp.commandv("af", "pre", "loudnorm")
		else
			mp.commandv("af", "remove", "loudnorm")
		end
	end
end

mp.observe_property("path", "string", check_achannels)
mp.observe_property("aid", "number", check_achannels)
