class_name AnimalPointers
extends RefCounted
## An animal owns at most one pointer, captured until release/cancel.
var owners: Dictionary = {}
var starts: Dictionary = {}

func press(pointer: int, animal: int, at: Vector2) -> bool:
	if owners.has(pointer) or animal in owners.values():
		return false
	owners[pointer] = animal
	starts[pointer] = at
	return true

func release(pointer: int) -> int:
	var animal: int = owners.get(pointer, -1)
	owners.erase(pointer)
	starts.erase(pointer)
	return animal

func clear() -> void:
	owners.clear()
	starts.clear()
