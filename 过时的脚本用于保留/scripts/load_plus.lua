--[[
SOURCE_ https://github.com/mpv-player/mpv/blob/master/TOOLS/lua/autoload.lua
COMMIT_ 3ba446d0b065f867ca262a2e05e4e8d24c7c0783
SOURCE_ https://github.com/rossy/mpv-open-file-dialog/blob/master/open-file-dialog.lua
COMMIT_ 04fe818fc703d8c5dcc3a6aabe1caeed8286bdbb
文档_ https://github.com/hooke007/MPV_lazy/discussions/106

功能集一：
  列表文件数量为1时自动填充同目录下的其它文件，可使用对应的 load_plus.conf 管理脚本设置。

功能集二：
  自定义快捷键 在mpv中唤起一个打开文件的窗口用于快速加载文件/网址

示例：在 input.conf 中另起写入下列内容
 w        script-binding load_plus/import_files   # 打开文件
 W        script-binding load_plus/import_url     # 打开地址
 CTRL+w   script-binding load_plus/append_aid     # 追加其它音轨（不切换）
 ALT+w    script-binding load_plus/append_sid     # 追加其它字幕（切换）
 e        script-binding load_plus/append_vfSub   # 装载次字幕（滤镜型）
 E        script-binding load_plus/toggle_vfSub   # 隐藏/显示 当前的次字幕（滤镜型）
 CTRL+e   script-binding load_plus/remove_vfSub   # 移除次字幕（滤镜型）
]]

local msg = require "mp.msg"
local options = require "mp.options"
local utils = require "mp.utils"

opt = {
	level = -1,              -- <-1|0|1> 自动填充的等级，分别对应 按预设条件/始终阻止/仅近似名文件
	video = true,            -- 是否填充视频
	video_ext = "default",   -- 允许的视频扩展名列表
	audio = false,           -- 是否填充音频
	audio_ext = "default",   -- 允许的视频扩展名列表
	image = false,           -- 是否填充图片
	image_ext = "default",   -- 允许的视频扩展名列表
	skip_hidden = true,      -- 跳过隐藏文件（当资源管理器内勾选“显示隐藏的文件”时无效）
	max_entries = 150        -- 当前条目前后各追加的文件数 
}
options.read_options(opt)

--
-- 单文件时自动补充队列
--

function Set (t)
	local set = {}
	for _, v in pairs(t) do set[v] = true end
	return set
end

function SetUnion (a,b)
	local res = {}
	for k in pairs(a) do res[k] = true end
	for k in pairs(b) do res[k] = true end
	return res
end

if opt.video_ext ~= "default" then
	local video_ext_tab = {}
	for x in opt.video_ext:gmatch("[^,]+") do
		table.insert(video_ext_tab, x)
	end
	EXTENSIONS_VIDEO = Set (video_ext_tab)
else
	EXTENSIONS_VIDEO = Set {
		"3g2","3gp",
		"amv","asf","avi",
		"f4v","flv",
		"m2ts","m4v","mkv","mov","mp4","mpeg","mpg",
		"ogv",
		"rm","rmvb",
		"ts",
		"vob",
		"webm","wmv",
		"y4m" }
end

if opt.audio_ext ~= "default" then
	local audio_ext_tab = {}
	for x in opt.audio_ext:gmatch("[^,]+") do
		table.insert(audio_ext_tab, x)
	end
	EXTENSIONS_AUDIO = Set (audio_ext_tab)
else
	EXTENSIONS_AUDIO = Set {
		"aac","aiff","alac","ape","au",
		"dsf",
		"flac",
		"m4a","mp3",
		"oga","ogg","ogm","opus",
		"tak","tta",
		"wav","wma","wv" }
end

if opt.image_ext ~= "default" then
	local image_ext_tab = {}
	for x in opt.image_ext:gmatch("[^,]+") do
		table.insert(image_ext_tab, x)
	end
	EXTENSIONS_IMAGE = Set (image_ext_tab)
else
	EXTENSIONS_IMAGE = Set {
		"apng","avif",
		"bmp",
		"gif",
		"j2k", "jfif","jp2","jpeg","jpg",
		"png",
		"svg",
		"tga","tif","tiff",
		"uci",
		"webp" }
end

EXTENSIONS = Set {}
if opt.video then EXTENSIONS = SetUnion(EXTENSIONS, EXTENSIONS_VIDEO) end
if opt.audio then EXTENSIONS = SetUnion(EXTENSIONS, EXTENSIONS_AUDIO) end
if opt.image then EXTENSIONS = SetUnion(EXTENSIONS, EXTENSIONS_IMAGE) end

function add_files(files)
	local oldcount = mp.get_property_number("playlist-count", 1)
	for i = 1, #files do
		mp.commandv("loadfile", files[i][1], "append")
		mp.commandv("playlist-move", oldcount + i - 1, files[i][2])
	end
end

function get_extension(path)
	match = string.match(path, "%.([^%.]+)$" )
	if match == nil then
		return "nomatch"
	else
		return match
	end
end

table.filter = function(t, iter)
	for i = #t, 1, -1 do
		if not iter(t[i]) then
			table.remove(t, i)
		end
	end
end

-- alphanum sorting for humans in Lua
-- http://notebook.kulchenko.com/algorithms/alphanumeric-natural-sorting-for-humans-in-lua

function alphanumsort(filenames)
	local function padnum(n, d)
		return #d > 0 and ("%03d%s%.12f"):format(#n, n, tonumber(d) / (10 ^ #d))
			or ("%03d%s"):format(#n, n)
	end

	local tuples = {}
	for i, f in ipairs(filenames) do
		tuples[i] = {f:lower():gsub("0*(%d+)%.?(%d*)", padnum), f}
	end
	table.sort(tuples, function(a, b)
		return a[1] == b[1] and #b[2] < #a[2] or a[1] < b[1]
	end)
	for i, tuple in ipairs(tuples) do filenames[i] = tuple[2] end
	return filenames
end

function get_playlist_filenames(playlist)
	local filenames = {}
	for i = 1, #playlist do
		local _, file = utils.split_path(playlist[i].filename)
		filenames[file] = true
	end
	return filenames
end

function find_and_add_entries()
	local path = mp.get_property("path", "")
	local dir, filename = utils.split_path(path)
	msg.trace(("dir: %s, filename: %s"):format(dir, filename))
	if opt.level == 0 then
		msg.verbose("自动队列中止：功能已禁用")
		return
	elseif #dir == 0 then
		msg.warn("自动队列中止：非本地路径")
		return
	end

	pl_count = mp.get_property_number("playlist-count", 1)
	if pl_count > 1 then
		msg.warn("自动队列中止：已手动创建/修改播放列表")
		return
	end

	local pl = mp.get_property_native("playlist", {})
	local pl_current = mp.get_property_number("playlist-pos-1", 1)
	msg.trace(("playlist-pos-1: %s, playlist: %s"):format(pl_current,
		utils.to_string(pl)))

	local files = utils.readdir(dir, "files")
	if files == nil then
		msg.info("自动队列：当前目录无其它文件")
		return
	end
	table.filter(files, function (v, k)
		-- The current file could be a hidden file, ignoring it doesn't load other
		-- files from the current directory.
		if (opt.skip_hidden and not (v == filename) and string.match(v, "^%.")) then
			return false
		end
		local ext = get_extension(v)
		if ext == nil then
			return false
		end
	if opt.level == 1 then
		local name = mp.get_property("filename")
		local namepre = string.sub(name, 1, 6)
		local namepre0 = string.gsub(namepre, "%p", "%%%1")
		for ext, _ in pairs(EXTENSIONS) do
			if string.match(name, ext.."$") ~= nil then
				if string.match(v, "^"..namepre0) == nil then
				return false
				end
			end
		end
	end
		return EXTENSIONS[string.lower(ext)]
	end)
	alphanumsort(files)

	if dir == "." then
		dir = ""
	end

	-- Find the current pl entry (dir+"/"+filename) in the sorted dir list
	local current
	for i = 1, #files do
		if files[i] == filename then
			current = i
			break
		end
	end
	if current == nil then
		return
	end
	msg.trace("自动队列：当前文件所处序列 "..current)

	local append = {[-1] = {}, [1] = {}}
	local filenames = get_playlist_filenames(pl)
	for direction = -1, 1, 2 do -- 2 iterations, with direction = -1 and +1
		for i = 1, opt.max_entries do
			local pos = current + i * direction
			local file = files[pos]
			if file == nil or file[1] == "." then
				break
			end

			local filepath = dir .. file
			-- skip files already in playlist
			if not filenames[file] then
				if direction == -1 then
					msg.info("自动队列 追加（前）" .. file)
					table.insert(append[-1], 1, {filepath, pos - 1})
				else
					msg.info("自动队列 追加（后）" .. file)
					if pl_count > 1 then
						table.insert(append[1], {filepath, pos - 1})
					else
						mp.commandv("loadfile", filepath, "append")
					end
				end
			end
		end
		if pl_count == 1 and direction == -1 and #append[-1] > 0 then
			for i = 1, #append[-1] do
				mp.commandv("loadfile", append[-1][i][1], "append")
			end
			mp.commandv("playlist-move", 0, current)
		end
	end

	if pl_count > 1 then
		add_files(append[1])
		add_files(append[-1])
	end
end


--
-- 弹出对话框加载文件
--

function import_files()
	local was_ontop = mp.get_property_native("ontop")
	if was_ontop then mp.set_property_native("ontop", false) end
	local res = utils.subprocess({
		args = {'powershell', '-NoProfile', '-Command', [[& {
			Trap {
				Write-Error -ErrorRecord $_
				Exit 1
			}
			Add-Type -AssemblyName PresentationFramework
			$u8 = [System.Text.Encoding]::UTF8
			$out = [Console]::OpenStandardOutput()
			$ofd = New-Object -TypeName Microsoft.Win32.OpenFileDialog
			$ofd.Multiselect = $true
			If ($ofd.ShowDialog() -eq $true) {
				ForEach ($filename in $ofd.FileNames) {
					$u8filename = $u8.GetBytes("$filename`n")
					$out.Write($u8filename, 0, $u8filename.Length)
				}
			}
		}]]},
		cancellable = false,
	})
	if was_ontop then mp.set_property_native("ontop", true) end
	if (res.status ~= 0) then return end
	local first_file = true
	for filename in string.gmatch(res.stdout, '[^\n]+') do
		mp.commandv("loadfile", filename, first_file and "replace" or "append")
		first_file = false
	end
end

function import_url()
	local was_ontop = mp.get_property_native("ontop")
	if was_ontop then mp.set_property_native("ontop", false) end
	local res = utils.subprocess({
		args = {'powershell', '-NoProfile', '-Command', [[& {
			Trap {
				Write-Error -ErrorRecord $_
				Exit 1
			}
			Add-Type -AssemblyName Microsoft.VisualBasic
			$u8 = [System.Text.Encoding]::UTF8
			$out = [Console]::OpenStandardOutput()
			$urlname = [Microsoft.VisualBasic.Interaction]::InputBox("输入地址", "打开", "https://")
			$u8urlname = $u8.GetBytes("$urlname")
			$out.Write($u8urlname, 0, $u8urlname.Length)
		}]]},
		cancellable = false,
	})
	if was_ontop then mp.set_property_native("ontop", true) end
	if (res.status ~= 0) then return end
	mp.commandv("loadfile", res.stdout)
end

function append_aid()
	local was_ontop = mp.get_property_native("ontop")
	if was_ontop then mp.set_property_native("ontop", false) end
	local res = utils.subprocess({
		args = {'powershell', '-NoProfile', '-Command', [[& {
			Trap {
				Write-Error -ErrorRecord $_
				Exit 1
			}
			Add-Type -AssemblyName PresentationFramework
			$u8 = [System.Text.Encoding]::UTF8
			$out = [Console]::OpenStandardOutput()
			$ofd = New-Object -TypeName Microsoft.Win32.OpenFileDialog
			$ofd.Multiselect = $false
			If ($ofd.ShowDialog() -eq $true) {
				ForEach ($filename in $ofd.FileNames) {
					$u8filename = $u8.GetBytes("$filename")
					$out.Write($u8filename, 0, $u8filename.Length)
				}
			}
		}]]},
		cancellable = false,
	})
	if was_ontop then mp.set_property_native("ontop", true) end
	if (res.status ~= 0) then return end
	for filename in string.gmatch(res.stdout, '[^\n]+') do
		mp.commandv("audio-add", filename, "auto")
	end
end

function append_sid()
	local was_ontop = mp.get_property_native("ontop")
	if was_ontop then mp.set_property_native("ontop", false) end
	local res = utils.subprocess({
		args = {'powershell', '-NoProfile', '-Command', [[& {
			Trap {
				Write-Error -ErrorRecord $_
				Exit 1
			}
			Add-Type -AssemblyName PresentationFramework
			$u8 = [System.Text.Encoding]::UTF8
			$out = [Console]::OpenStandardOutput()
			$ofd = New-Object -TypeName Microsoft.Win32.OpenFileDialog
			$ofd.Multiselect = $false
			If ($ofd.ShowDialog() -eq $true) {
				ForEach ($filename in $ofd.FileNames) {
					$u8filename = $u8.GetBytes("$filename")
					$out.Write($u8filename, 0, $u8filename.Length)
				}
			}
		}]]},
		cancellable = false,
	})
	if was_ontop then mp.set_property_native("ontop", true) end
	if (res.status ~= 0) then return end
	for filename in string.gmatch(res.stdout, '[^\n]+') do
		mp.commandv("sub-add", filename, "cached")
	end
end

function append_vfSub()
	local was_ontop = mp.get_property_native("ontop")
	if was_ontop then mp.set_property_native("ontop", false) end
	local res = utils.subprocess({
		args = {'powershell', '-NoProfile', '-Command', [[& {
			Trap {
				Write-Error -ErrorRecord $_
				Exit 1
			}
			Add-Type -AssemblyName PresentationFramework
			$u8 = [System.Text.Encoding]::UTF8
			$out = [Console]::OpenStandardOutput()
			$ofd = New-Object -TypeName Microsoft.Win32.OpenFileDialog
			$ofd.Multiselect = $false
			If ($ofd.ShowDialog() -eq $true) {
				ForEach ($filename in $ofd.FileNames) {
					$u8filename = $u8.GetBytes("$filename")
					$out.Write($u8filename, 0, $u8filename.Length)
				}
			}
		}]]},
		cancellable = false,
	})
	if was_ontop then mp.set_property_native("ontop", true) end
	if (res.status ~= 0) then return end
	for filename in string.gmatch(res.stdout, '[^\n]+') do
		local vfSub = "vf append ``@LUA-load_plus:subtitles=filename=\"" .. res.stdout .. "\"``"
		mp.command(vfSub)
	end
end

function filter_state(label, key, value)
	local filters = mp.get_property_native("vf")
	for _, filter in pairs(filters) do
		if filter["label"] == label and (not key or key and filter[key] == value) then
			return true
		end
	end
	return false
end

function toggle_vfSub()
	local vfSub = "vf toggle @LUA-load_plus"
	if filter_state("LUA-load_plus") then mp.command(vfSub) end
end

function remove_vfSub()
	local vfSub = "vf remove @LUA-load_plus"
	if filter_state("LUA-load_plus") then mp.command(vfSub) end
end


mp.register_event("end-file", remove_vfSub)

mp.register_event("start-file", find_and_add_entries)

mp.add_key_binding(nil, "import_files", import_files)
mp.add_key_binding(nil, "import_url", import_url)
mp.add_key_binding(nil, "append_aid", append_aid)
mp.add_key_binding(nil, "append_sid", append_sid)
mp.add_key_binding(nil, "append_vfSub", append_vfSub)
mp.add_key_binding(nil, "toggle_vfSub", toggle_vfSub)
mp.add_key_binding(nil, "remove_vfSub", remove_vfSub)
