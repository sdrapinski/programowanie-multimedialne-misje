from OpenGL.GL import *
import glfw
import glm

from helpers.shaders import DemoShaders
from helpers.models import *

teapot = Teapot()
table = Cube()
leg = Cube()

speed_y = 0.0  # Prędkość obrotu wokół osi Y [rad/s]
speed_x = 0.0  # Prędkość obrotu wokół osi X [rad/s]

def key_callback(window, key, scancode, action, mods):
	global speed_y, speed_x
	if action == glfw.PRESS:
		if key == glfw.KEY_LEFT:
			speed_y = -3.14
		if key == glfw.KEY_RIGHT:
			speed_y = 3.14
		if key == glfw.KEY_UP:
			speed_x = -3.14
		if key == glfw.KEY_DOWN:
			speed_x = 3.14
	if action == glfw.RELEASE:
		if key == glfw.KEY_LEFT or key == glfw.KEY_RIGHT:
			speed_y = 0.0
		if key == glfw.KEY_UP or key == glfw.KEY_DOWN:
			speed_x = 0.0

def init_opengl_program(window):
	glClearColor(0, 0, 0, 1)
	DemoShaders.initShaders("helpers/shaders/")
	glfw.set_key_callback(window, key_callback)


def draw_scene(window, angle_x, angle_y):
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	V = glm.lookAt(
		glm.vec3(0.0, 0.0, -5.0),
		glm.vec3(0.0, 0.0, 0.0),
		glm.vec3(0.0, 1.0, 0.0)
	)
	P = glm.perspective(glm.radians(50.0), 1.0, 1.0, 50.0)

	DemoShaders.spConstant.use()
	glUniformMatrix4fv(DemoShaders.spConstant.u("P"), 1, GL_FALSE, P.to_list())
	glUniformMatrix4fv(DemoShaders.spConstant.u("V"), 1, GL_FALSE, V.to_list())

	M_scene = glm.rotate(angle_y, glm.vec3(0, 1, 0)) * glm.rotate(angle_x, glm.vec3(1, 0, 0))


	M_teapot = M_scene
	glUniformMatrix4fv(DemoShaders.spConstant.u("M"), 1, GL_FALSE, M_teapot.to_list())

	teapot.drawSolid()

	#stol
	
	M_table = M_scene
	M_table = glm.scale(glm.mat4(1.0), glm.vec3(1, 0.1, 1))
	M_table *= glm.rotate(angle_y, glm.vec3(0, 1, 0)) * glm.rotate(angle_x, glm.vec3(1, 0, 0))
	M_table = glm.translate(M_table, glm.vec3(0.0, -5, 0.0))

	glUniformMatrix4fv(DemoShaders.spConstant.u("M"), 1, GL_FALSE, M_table.to_list())
	table.drawSolid()

	#nogi od stolu
	
	# Renderowanie nóg stołu
	leg_scale_x = 0.1  # Skala szerokości nogi
	leg_scale_z = 0.1  # Skala głębokości nogi
	leg_scale_y = 0.9  # Skala wysokości nogi
	leg_position_y = -2.0 + 0.5 * leg_scale_y  # Wysokość nóg na poziomie blatu stołu

	# Rysowanie czterech nóg stołu w odpowiednich miejscach
	for leg_position_x in [-2, 2]:
		for leg_position_z in [-2, 2]:
			M_leg = glm.mat4(1.0)
			M_leg = glm.translate(M_leg, glm.vec3(leg_position_x * 0.4, leg_position_y, leg_position_z * 0.4))
			M_leg *= glm.rotate(angle_y, glm.vec3(0, 1, 0)) * glm.rotate(angle_x, glm.vec3(1, 0, 0))
			M_leg = glm.scale(M_leg, glm.vec3(leg_scale_x, leg_scale_y, leg_scale_z))
			glUniformMatrix4fv(DemoShaders.spConstant.u("M"), 1, GL_FALSE, M_leg.to_list())
			leg.drawSolid()

	glfw.swap_buffers(window)

def free_opengl_program(window):
	# Możesz dodać odpowiednie czyszczenie zasobów tutaj, jeśli jest to konieczne
	pass

def main():
	glfw.init()
	window = glfw.create_window(500, 500, "Szymon Drapinski Herbata", None, None)
	glfw.make_context_current(window)
	glfw.swap_interval(1)

	init_opengl_program(window)

	glfw.set_time(0)

	angle_x = 0.0
	angle_y = 0.0

	while not glfw.window_should_close(window):
		time = glfw.get_time()
		glfw.set_time(0.0) # Wyzeruj licznik czasu

		angle_x += speed_x * time # Aktualizuj kat obrotu wokół osi X zgodnie z prędkością obrotu
		angle_y += speed_y * time # Aktualizuj kat obrotu wokół osi Y zgodnie z prędkością obrotu

		draw_scene(window, angle_x, angle_y)
		glfw.poll_events()


	free_opengl_program(window)
	glfw.terminate()


if __name__ == "__main__":
	main()
