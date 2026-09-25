extends SceneTree
const Pointers = preload("res://scripts/pointers.gd")

func _initialize() -> void:
	var p := Pointers.new()
	assert(p.press(1, 0, Vector2(10, 20)))
	assert(not p.press(2, 0, Vector2.ZERO), "Extra finger cannot steal an animal")
	assert(p.press(3, 1, Vector2(80, 20)), "Both animals can be held")
	assert(not p.press(1, 1, Vector2.ZERO), "Captured pointer cannot transfer")
	assert(p.release(2) == -1, "Ignored finger release has no effect")
	assert(p.owners.size() == 2)
	assert(p.release(1) == 0)
	assert(p.owners[3] == 1)
	p.clear()
	assert(p.owners.is_empty() and p.starts.is_empty(), "Cancellation clears all state")
	assert(p.press(-1, 0, Vector2.ZERO), "Mouse uses the same ownership path")
	assert(p.release(-1) == 0)
	print("PASS: pointer ownership, extra fingers, release, cancellation, mouse")
	quit()
