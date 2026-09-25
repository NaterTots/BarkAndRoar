extends Node2D

const Face = preload("res://scripts/animal.gd")
const Pointers = preload("res://scripts/pointers.gd")
var animals: Array[AnimalFace] = []
var panels: Array[Rect2] = []
var pointers := Pointers.new()
var playing := false
var web_callback: JavaScriptObject
var qa := false
var qa_time := 0.0

func _ready() -> void:
	for i in range(2):
		var animal := Face.new()
		animal.lion = i == 0
		animals.append(animal)
		add_child(animal)
	get_viewport().size_changed.connect(layout)
	layout()
	if OS.has_feature("web"):
		web_callback = JavaScriptBridge.create_callback(_web_reset)
		JavaScriptBridge.get_interface("window").barkReset = web_callback
		qa = bool(JavaScriptBridge.eval("new URLSearchParams(location.search).has('qa')"))
		JavaScriptBridge.eval("window.barkReady = true")

func _web_reset(_args: Array) -> void:
	reset_input(true)
	playing = false
	queue_redraw()

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT or what == NOTIFICATION_APPLICATION_PAUSED:
		reset_input(true)
		playing = false
		queue_redraw()

func reset_input(stop_audio: bool = false) -> void:
	pointers.clear()
	for animal in animals:
		animal.reset(stop_audio)

func layout() -> void:
	reset_input()
	var size := get_viewport_rect().size
	var landscape := size.x >= size.y
	var half := size * (Vector2(0.5, 1) if landscape else Vector2(1, 0.5))
	panels = [Rect2(Vector2.ZERO, half), Rect2(Vector2(half.x, 0) if landscape else Vector2(0, half.y), half)]
	for i in range(2):
		animals[i].home = panels[i].get_center()
		animals[i].face_scale = minf(half.x * 0.73 / 350.0, half.y * 0.73 / 350.0)
		animals[i].offset = Vector2.ZERO
	queue_redraw()

func panel_at(at: Vector2) -> int:
	for i in range(panels.size()):
		if panels[i].has_point(at):
			return i
	return -1

func down(pointer: int, at: Vector2) -> void:
	if not playing:
		playing = true
		queue_redraw()
		return
	var index := panel_at(at)
	if index >= 0 and pointers.press(pointer, index, at):
		animals[index].held = true
		animals[index].react()

func move(pointer: int, at: Vector2) -> void:
	if not pointers.owners.has(pointer):
		return
	var index: int = pointers.owners[pointer]
	var relative: Vector2 = at - pointers.starts[pointer]
	if relative.length() < 9.0:
		relative = Vector2.ZERO
	var limit := minf(panels[index].size.x, panels[index].size.y) * 0.10
	animals[index].target_offset = relative.limit_length(limit)

func up(pointer: int) -> void:
	var index := pointers.release(pointer)
	if index >= 0:
		animals[index].reset()

func _input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		if event.canceled or not event.pressed:
			up(event.index)
		else:
			down(event.index, event.position)
	elif event is InputEventScreenDrag:
		move(event.index, event.position)
	elif event is InputEventMouseButton and event.device != InputEvent.DEVICE_ID_EMULATION:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				down(-1, event.position)
			else:
				up(-1)
	elif event is InputEventMouseMotion and event.device != InputEvent.DEVICE_ID_EMULATION:
		move(-1, event.position)
	elif event is InputEventKey and event.pressed and not event.echo:
		if not playing and event.keycode in [KEY_SPACE, KEY_ENTER]:
			playing = true
			queue_redraw()

func _draw() -> void:
	if panels.size() != 2:
		return
	draw_rect(panels[0], Color("b9d7cc"))
	draw_rect(panels[1], Color("f2c7b5"))
	# The initial play affordance is drawn above the faces by a separate canvas layer.

func _process(delta: float) -> void:
	queue_redraw()
	if not has_node("PlayOverlay"):
		var overlay := Node2D.new()
		overlay.name = "PlayOverlay"
		overlay.z_index = 10
		overlay.draw.connect(func():
			if not playing:
				var center := get_viewport_rect().size / 2
				overlay.draw_rect(get_viewport_rect(), Color(0.99, 0.96, 0.88, 0.50))
				overlay.draw_circle(center + Vector2(0, 7), 65, Color(0.22, 0.18, 0.19, 0.15))
				overlay.draw_circle(center, 65, Color("fff7e6"))
				overlay.draw_arc(center, 65, 0, TAU, 96, Face.INK, 5, true)
				overlay.draw_colored_polygon(PackedVector2Array([center + Vector2(-16, -26), center + Vector2(-16, 26), center + Vector2(29, 0)]), Face.INK)
		)
		add_child(overlay)
	get_node("PlayOverlay").queue_redraw()
	if qa:
		qa_time += delta
		if qa_time > 0.1:
			qa_time = 0.0
			var state := {"playing": playing, "owners": pointers.owners.size(), "animals": []}
			for animal in animals:
				state.animals.append({"held": animal.held, "offset": [animal.offset.x, animal.offset.y], "activations": animal.activations, "audio": animal.player.playing, "sound_starts": animal.sound_starts, "players": animal.get_child_count()})
			JavaScriptBridge.eval("window.barkState = " + JSON.stringify(state))
