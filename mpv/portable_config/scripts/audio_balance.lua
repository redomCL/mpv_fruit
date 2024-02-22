--[[

SOURCE_ https://github.com/wiiaboo/mpv-scripts/blob/master/audio-balance.lua
COMMIT_ 20220811 03cfc0e39682a73d9d24a6e01a3c02716a019d1d

声道平衡
立体声使用的是仅削弱单边的逻辑，但多声道仍沿用了原设计（存在问题）中的混合思路

示例在 input.conf 中写入 ：
Ctrl+A        script-binding audio_balance/bal2l       # 平衡偏左（步进1%，按住可持续触发）
Alt+A         script-binding audio_balance/bal2r       # 平衡偏右（...）
Ctrl+Alt+A    script-binding audio_balance/bal_reset   # 重置平衡

]]

local options = require("mp.options")

local opts = {
	forcelayout = "",    -- if empty, will use the same layout as the original audio
	auto_reset = true,   -- 自动重置
}

options.read_options(opts)

local left = 0.5
local right = 0.5

local function add_left_channel_stereo(left_ch_name, right_ch_name)
	if left <= right then 
		ratio = left/right
		return string.format("%s=%.3f*%s", left_ch_name, ratio, left_ch_name)
	else
		return string.format("%s=%s", left_ch_name, left_ch_name)
	end
end

local function add_right_channel_stereo(left_ch_name, right_ch_name)
	if left > right then
		ratio = right/left 
		return string.format("%s=%.3f*%s", right_ch_name, ratio, right_ch_name)
	else
		return string.format("%s=%s", right_ch_name, right_ch_name)
	end
end

local function add_left_channel(left_ch_name, right_ch_name)
	return string.format("%s=%.1f*%s+%.1f*%s",
		left_ch_name,
		math.max(0,math.min(1,left*2)), left_ch_name,
		math.max(0,math.min(1,(right-0.5)*2)), right_ch_name)
end

local function add_right_channel(left_ch_name, right_ch_name)
	return string.format("%s=%.1f*%s+%.1f*%s",
		right_ch_name,
		math.max(0,math.min(1,(left-0.5)*2)), left_ch_name,
		math.max(0,math.min(1,right*2)), right_ch_name)
end

local function update_filter()
	local graph = {}
	local channels =
		opts.forcelayout ~= "" and opts.forcelayout or
		mp.get_property("audio-params/hr-channels", "stereo")
	if channels == "mono" then
		return
	end

	if channels == "stereo" then
		graph[1] = add_left_channel_stereo('FL', 'FR')
		graph[2] = add_right_channel_stereo('FL', 'FR')
	else
		graph[1] = add_left_channel('FL', 'FR')
		graph[2] = add_right_channel('FL', 'FR')
	end

	if channels == "3.0" or
		channels == "3.0(back)" or
		channels == "3.1" or
		channels == "5.0" or
		channels == "5.0(side)" or
		channels == "4.1" or
		channels == "5.1" or
		channels == "5.1(side)" or
		channels == "6.0" or
		channels == "6.0(front)" or
		channels == "hexagonal" or
		channels == "6.1" or
		channels == "7.0" or
		channels == "7.0(front)" or
		channels == "7.1" or
		channels == "7.1(wide)" or
		channels == "7.1(side-side)" or
		channels == "octagonal" then
		graph[#graph+1] = 'FC=FC'
	end

	if channels == "2.1" or
		channels == "3.1" or
		channels == "4.1" or
		channels == "5.1" or
		channels == "5.1(side)" or
		channels == "6.1" or
		channels == "6.1(front)" or
		channels == "7.1" or
		channels == "7.1(wide)" or
		channels == "7.1(side-side)" then
		graph[#graph+1] = 'LFE=LFE'
	end

	if channels == "3.0(back)" or
		channels == "4.0" or
		channels == "4.1" or
		channels == "6.0" or
		channels == "hexagonal" or
		channels == "6.1" or
		channels == "6.1(back)" or
		channels == "octagonal" then
		graph[#graph+1] = 'BC=BC'
	end

	if channels == "quad" or
		channels == "5.0" or
		channels == "5.1" or
		channels == "hexagonal" or
		channels == "6.1(back)" or
		channels == "7.0" or
		channels == "7.1" or
		channels == "7.1(wide)" or
		channels == "octagonal" then
		graph[#graph+1] = add_left_channel('BL', 'BR')
		graph[#graph+1] = add_right_channel('BL', 'BR')
	end

	if channels == "quad(side)" or
		channels == "5.0(side)" or
		channels == "5.1(side)" or
		channels == "hexagonal" or
		channels == "6.0" or
		channels == "6.0(front)" or
		channels == "6.1" or
		channels == "6.1(front)" or
		channels == "7.0" or
		channels == "7.0(front)" or
		channels == "7.1" or
		channels == "7.1(wide-side)" or
		channels == "octagonal" then
		graph[#graph+1] = add_left_channel('SL', 'SR')
		graph[#graph+1] = add_right_channel('SL', 'SR')
	end

	if channels == "6.0(front)" or
		channels == "6.1(front)" or
		channels == "7.0(front)" or
		channels == "7.1(wide)" or
		channels == "7.1(wide-side)" then
		graph[#graph+1] = add_left_channel('FLC', 'FRC')
		graph[#graph+1] = add_right_channel('FLC', 'FRC')
	end

	mp.command(string.format("no-osd af append @LUA-audio_balance:lavfi=[pan=%s|%s]",
		channels, table.concat(graph, "|")))

	mp.commandv("show-text", string.format("声道平衡：\n- 左：%.0f%%\n- 右：%.0f%%", left*100, right*100))
end

local function change_balance(val)
	val = tonumber(val)
	if not val or (val > 1 or val < -1) then
		mp.msg.warn("Parameter should be a number between -1.0 and 1.0 (was "..val..")")
		return
	end
	left  = math.max(0,math.min(1,left + val * -1))
	right = math.max(0,math.min(1,right + val))
	update_filter()
end

local function filter_state(label, key, value)
	local filters = mp.get_property_native("af")
	for _, filter in pairs(filters) do
		if filter["label"] == label and (not key or key and filter[key] == value) then
			return true
		end
	end
	return false
end

local function reset_balance(auto)
	if filter_state("LUA-audio_balance") then
		mp.commandv("no-osd", "af", "remove", "@LUA-audio_balance")
		left = 0.5
		right = 0.5
		mp.commandv("show-text", string.format("声道平衡：\n- 左：%.0f%%\n- 右：%.0f%%", left*100, right*100))
		if auto then
			mp.msg.info("音轨变动，已重置平衡")
		end
	else
		return
	end
end


mp.register_script_message(mp.get_script_name(), change_balance)

mp.add_key_binding(nil, "bal2l", function() change_balance(-0.01); end, { repeatable = true })
mp.add_key_binding(nil, "bal2r", function() change_balance(0.01); end, { repeatable = true })
mp.add_key_binding(nil, "bal_reset", reset_balance)

if opts.auto_reset then
	mp.observe_property("path", "string", function() reset_balance(true) end)
	mp.observe_property("aid", "number", function() reset_balance(true) end)
end
