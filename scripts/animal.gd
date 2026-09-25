class_name AnimalFace
extends Node2D
## Original layered vector drawing, animated without allocating tweens.
const INK := Color("382d32")
var lion := true
var held := false
var home := Vector2.ZERO
var target_offset := Vector2.ZERO
var offset := Vector2.ZERO
var face_scale := 1.0
var reaction := 0.0
var age := 0.0
var activations := 0
var sound_starts := 0
var player: AudioStreamPlayer

func _ready() -> void:
	player = AudioStreamPlayer.new()
	player.stream = load("res://assets/audio/roar.wav" if lion else "res://assets/audio/bark.wav")
	player.playback_type = AudioServer.PLAYBACK_TYPE_STREAM
	player.max_polyphony = 1
	player.volume_db = -3.0
	add_child(player)

func react() -> void:
	reaction = 0.72 if lion else 0.52
	activations += 1
	if not player.playing:
		sound_starts += 1
		player.play()

func reset(stop_audio: bool = false) -> void:
	held = false
	target_offset = Vector2.ZERO
	if stop_audio:
		player.stop()
		reaction = 0.0

func _process(delta: float) -> void:
	age += delta
	reaction = maxf(0.0, reaction - delta)
	offset = offset.lerp(target_offset, 1.0 - exp(-15.0 * delta))
	position = home + offset
	rotation = lerpf(rotation, clampf(offset.x / maxf(face_scale * 160.0, 1.0), -1.0, 1.0) * deg_to_rad(8.0), 1.0 - exp(-16.0 * delta))
	var bounce := sin(reaction * 19.0) * reaction * 0.09
	scale = Vector2(1.0 + bounce, 1.0 - bounce) * face_scale
	queue_redraw()

func oval(center: Vector2, radius: Vector2, color: Color, outline: float = 7.0) -> void:
	var points := PackedVector2Array()
	for i in range(65):
		var angle := TAU * i / 64.0
		points.append(center + Vector2(cos(angle), sin(angle)) * radius)
	draw_colored_polygon(points, color)
	if outline > 0:
		draw_polyline(points, INK, outline, true)

func curve(points: Array[Vector2], color: Color = INK, width: float = 6.0) -> void:
	# Quadratic Bezier sampled for the small smile curves.
	var line := PackedVector2Array()
	for i in range(25):
		var t := i / 24.0
		line.append((1-t)*(1-t)*points[0] + 2*(1-t)*t*points[1] + t*t*points[2])
	draw_polyline(line, color, width, true)

func _draw() -> void:
	var wobble := sin(reaction * 22.0) * reaction * 5.0
	if lion:
		# Scalloped mane, one continuous silhouette.
		var mane := PackedVector2Array()
		for i in range(193):
			var a := TAU * i / 192.0
			var r := 166.0 + 9.0 * cos(a * 12.0)
			mane.append(Vector2(cos(a), sin(a)) * r + Vector2(wobble, 0))
		draw_colored_polygon(mane, Color("d8753f"))
		draw_polyline(mane, INK, 8.0, true)
		oval(Vector2(-86, -88), Vector2(36, 38), Color("f4bd5a"))
		oval(Vector2(86, -88), Vector2(36, 38), Color("f4bd5a"))
		oval(Vector2(-86, -88), Vector2(17, 20), Color("c66a43"), 0)
		oval(Vector2(86, -88), Vector2(17, 20), Color("c66a43"), 0)
		oval(Vector2(0, 3), Vector2(115, 118), Color("f6c65f"))
	else:
		oval(Vector2(0, 0), Vector2(117, 130), Color("f4d9a4"))
		oval(Vector2(-115, -29 + wobble), Vector2(39, 95), Color("745046"))
		oval(Vector2(115, -29 - wobble), Vector2(39, 95), Color("745046"))
		oval(Vector2(48, -26), Vector2(40, 51), Color("d59a60"), 0)
		oval(Vector2(-9, -60), Vector2(25, 63), Color("fff0d3"), 0)
	# Eyes blink occasionally; their highlight makes a warm, direct gaze.
	var blink := fmod(age + (1.7 if lion else 0.0), 5.8) < 0.13
	for x in [-43.0, 43.0]:
		if blink:
			curve([Vector2(x-13,-29), Vector2(x,-18), Vector2(x+13,-29)])
		else:
			oval(Vector2(x, -29), Vector2(18, 24), Color("fffaf0"), 5)
			oval(Vector2(x+2, -25), Vector2(9, 14), INK, 0)
			oval(Vector2(x+5, -31), Vector2(3.8, 5), Color.WHITE, 0)
		curve([Vector2(x-14,-64), Vector2(x,-72), Vector2(x+12,-65)], INK, 5)
	# Soft cheeks and paired muzzle lobes.
	oval(Vector2(-73, 27), Vector2(17, 11), Color("e79a74"), 0)
	oval(Vector2(73, 27), Vector2(17, 11), Color("e79a74"), 0)
	if reaction > 0.06:
		oval(Vector2(0, 67), Vector2(28 if lion else 24, 32 if lion else 29), INK, 0)
		oval(Vector2(0, 84), Vector2(17, 11), Color("ec9299"), 0)
	elif not lion:
		oval(Vector2(0, 71), Vector2(19, 26), INK, 0)
		oval(Vector2(0, 78), Vector2(14, 17), Color("ec9299"), 0)
	oval(Vector2(-24, 40), Vector2(36, 28), Color("fff0cf"), 0)
	oval(Vector2(24, 40), Vector2(36, 28), Color("fff0cf"), 0)
	oval(Vector2(0, 21), Vector2(24, 16) if lion else Vector2(29, 21), INK, 0)
	oval(Vector2(-7, 15), Vector2(8, 4), Color("806468"), 0)
	draw_line(Vector2(0,32), Vector2(0,49), INK, 5, true)
	curve([Vector2(-34,50), Vector2(-16,69 if held else 66), Vector2(0,49)])
	curve([Vector2(0,49), Vector2(16,69 if held else 66), Vector2(34,50)])
	for x in [-39.0, -25.0, 25.0, 39.0]:
		draw_circle(Vector2(x, 38), 2.3, INK)
