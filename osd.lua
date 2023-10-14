local ipairs,loadfile,pairs,pcall,tonumber,tostring = ipairs,loadfile,pairs,pcall,tonumber,tostring
local debug,io,math,os,string,table,utf8 = debug,io,math,os,string,table,utf8
local min,max,floor,ceil,huge = math.min,math.max,math.floor,math.ceil,math.huge
local mp      = require 'mp'
local assdraw = require 'mp.assdraw'
local msg     = require 'mp.msg'
local opt     = require 'mp.options'
local utils   = require 'mp.utils'


local ov = mp.create_osd_overlay('ass-events')
local timer = 0
local timerdec = 1
local ismessage = false

local mode='never'

function ass_escape(str, replace_newline)
    if replace_newline == true then replace_newline = "\\\239\187\191n" end
    str = str:gsub('[\\{}\n]', {
        ['\\'] = '\\\239\187\191',
        ['{'] = '\\{',
        ['}'] = '\\}',
        ['\n'] = '\239\187\191\\N',
    })
    str = str:gsub('\\N ', '\\N\\h')
    str = str:gsub('^ ', '\\h')
    if replace_newline then
        str = str:gsub("\\N", replace_newline)
    end
    return str
end

local osdtimer = mp.add_periodic_timer(0.1, function()
    
    if timer <= 0 then
        ov:remove()        
        ismessage=false
        timer=0
    else
        local nexttimer = timer-timerdec
        local val     = tostring(timer)
        local nextval = tostring(nexttimer)
        if ismessage == false then
            updateseekdata()
        end
        ov.data = ov.data:gsub("\\blur" .. val, "\\blur" .. nextval)
        ov.data = ov.data:gsub("\\bord" .. val, "\\bord" .. nextval)
        ov:update()
        timer = nexttimer
    end

    
end)

local ass_set_color = function (idx, color)
    assert(color:len() == 8 or color:len() == 6)
    local ass = ""
    -- Set alpha value (if present)
    if color:len() == 8 then
        local alpha = 0xff - tonumber(color:sub(7, 8), 16)
        ass = ass .. string.format("\\%da&H%X&", idx, alpha)
    end
    -- Swizzle RGB to BGR and build ASS string
    color = color:sub(5, 6) .. color:sub(3, 4) .. color:sub(1, 2)
    return "{" .. ass .. string.format("\\%dc&H%s&", idx, color) .. "}"
end

function osd_message(text)

    local osd_w, osd_h = mp.get_property("osd-width"), mp.get_property("osd-height")

    if osd_w == nil or osd_w == 0  then
        do return end
    end

    timer = 25
    ov.res_x = osd_w
    ov.res_y = osd_h

    local p1x = 1
    local p1y = 1
    local p2x = osd_w-1
    local p2y = osd_h-1

    ass = assdraw.ass_new()
    ass:new_event()

    ass:pos(0, 0)

    ass:new_event()

    ass:pos(10, 10)

    local style = "{\\bord2\\fs" .. '18' .. "}"


    ass:append(style .. ass_escape(text,false))
    ismessage=true
    ass:pos(0, 0)


    ov.data = ass.text

    osdtimer:kill()
    ov:update()
    osdtimer:resume()

end

function focus_hint()
    if mode == 'never' then
        do return end
    end
    local osd_w, osd_h = mp.get_property("osd-width"), mp.get_property("osd-height")
    
    if osd_w == nil or osd_w == 0  then
        do return end 
    end

    timer = 25
    ov.res_x = osd_w
    ov.res_y = osd_h

    local p1x = 1
    local p1y = 1
    local p2x = osd_w-1
    local p2y = osd_h-1

    ass = assdraw.ass_new()
    ass:new_event()

    ass:draw_start()

    ass:pos(0, 0)


    ass:append(ass_set_color(1, "000000DD"))
    ass:append(ass_set_color(3, "000000DD"))
    ass:append("{\\blur" .. tostring(timer) .. "\\bord" .. tostring(timer) .. "}")

    local l = math.min(tonumber(p1x), tonumber(p2x))
    local r = math.max(tonumber(p1x), tonumber(p2x))
    local u = math.min(tonumber(p1y), tonumber(p2y))
    local d = math.max(tonumber(p1y), tonumber(p2y))

    ass:rect_cw(0, 0, l, osd_h)
    ass:rect_cw(r, 0, osd_w, osd_h)
    ass:rect_cw(l, 0, r, u)
    ass:rect_cw(l, d, r, osd_h)

    ass:draw_stop()
    ass:pos(0, 0)

    ass:new_event()

    ass:pos(10, 10)

    local style = "{\\bord2\\fs" .. '18' .. "}"

    local title = mp.get_property_osd("filename")
    title = mp.get_property_osd("path") .. '\\' .. title
    ismessage=false
    title = ass_escape(title,true)

    ass:append(style .. title)

    ass:pos(0, 0)


    ov.data = ass.text

    osdtimer:kill()
    ov:update()
    osdtimer:resume()
end


function focus_hint_remove()
    timer=0
end

function updateseekdata()
    local pc = mp.get_property("percent-pos")

    if mode == 'never' then
        do return end
    end

    if tonumber(pc) then

        local osd_w, osd_h = mp.get_osd_size()

        if osd_w == nil or osd_w == 0  then
            do return end 
        end

        ass = assdraw.ass_new()
        ass:new_event()
        ass:draw_start()
        ass:pos(0, 0)

        ass:append(ass_set_color(1, "FFFFFFDD"))
        ass:append(ass_set_color(3, "000000DD"))
        ass:append("{\\blur" .. tostring(timer) .. "\\bord" .. tostring(timer) .. "}")
        ass:pos(0, 0)

        ass:rect_cw(0, osd_h-5, osd_w*(tonumber(pc)/100), osd_h-4)

        ass:draw_stop()
        ass:pos(0, 0)

        ov.res_x = osd_w
        ov.res_y = osd_h

        ass:pos(0, 0)

        ass:new_event()

        ass:pos(10, 10)

        local style = "{\\bord2\\fs" .. '18' .. "}"

        local title = mp.get_property_osd("filename")
        title = mp.get_property_osd("path") .. '\\' .. title
        ismessage=false
        title = ass_escape(title,true)

        ass:append(style .. title)

        ass:pos(0, 0)

        ov.data = ass.text
    end

end

function seekhandler()
    if mode == 'never' then
        do return end
    end
    local pc = mp.get_property("percent-pos")
    timer = 15
    if tonumber(pc) then
        updateseekdata()
        osdtimer:kill()
        ov:update()
        osdtimer:resume()
    end
end

function visibility_mode(vismode)
    mode = vismode
end

mp.register_event("seek", seekhandler)
mp.register_event("start-file", seekhandler)
mp.register_script_message("osd_rootmotion",  seekhandler)
mp.register_script_message("osd_message",     osd_message)
mp.register_script_message("osd_mode",        visibility_mode)
mp.register_script_message("osd_focus",       focus_hint)
mp.register_script_message("osd_defocus",     focus_hint_remove)

