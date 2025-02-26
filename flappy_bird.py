import pygame
import random
import os
import time
import neat
import pickle
pygame.font.init()

width = 600
height = 800
floor_y = 730
score_font = pygame.font.SysFont("cairo", 50)
end_font = pygame.font.SysFont("cairo", 70)
button_font = pygame.font.SysFont("cairo", 30)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

pipe_image = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
bg_image = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
base_image = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())

gen = 0

class Bird:
    max_tilt = 25
    images = bird_images
    tilt_speed = 20
    anim_time = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_number = 0
        self.velocity = 0
        self.start_height = self.y
        self.image_index = 0
        self.image = self.images[0]

    def jump(self):
        self.velocity = -10.5
        self.tick_number = 0
        self.start_height = self.y

    def move(self):
        self.tick_number += 1

        dy = self.velocity*(self.tick_number) + 0.5*(3)*(self.tick_number)**2

        if dy >= 16:
            dy = (dy/abs(dy)) * 16

        if dy < 0:
            dy -= 2

        self.y = self.y + dy

        if dy < 0 or self.y < self.start_height + 50:
            if self.tilt < self.max_tilt:
                self.tilt = self.max_tilt
        else:
            if self.tilt > -90:
                self.tilt -= self.tilt_speed

    def draw(self, win):
        self.image_index += 1

        if self.image_index <= self.anim_time:
            self.image = self.images[0]
        elif self.image_index <= self.anim_time*2:
            self.image = self.images[1]
        elif self.image_index <= self.anim_time*3:
            self.image = self.images[2]
        elif self.image_index <= self.anim_time*4:
            self.image = self.images[1]
        elif self.image_index == self.anim_time*4 + 1:
            self.image = self.images[0]
            self.image_index = 0

        if self.tilt <= -80:
            self.image = self.images[1]
            self.image_index = self.anim_time*2


        blitRotateCenter(win, self.image, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Pipe():
    pipe_gap = 200
    pipe_speed = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.pipe_top_img = pygame.transform.flip(pipe_image, False, True)
        self.pipe_bottom_img = pipe_image

        self.has_passed = False

        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top_img.get_height()
        self.bottom = self.height + self.pipe_gap

    def move(self):
        self.x -= self.pipe_speed

    def draw(self, win):
        win.blit(self.pipe_top_img, (self.x, self.top))
        win.blit(self.pipe_bottom_img, (self.x, self.bottom))


    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top_img)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom_img)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask,top_offset)

        if bottom_point or top_point:
            return True

        return False

class Base:
    base_speed = 5
    base_width = base_image.get_width()
    image = base_image

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.base_width

    def move(self):
        self.x1 -= self.base_speed
        self.x2 -= self.base_speed
        if self.x1 + self.base_width < 0:
            self.x1 = self.x2 + self.base_width

        if self.x2 + self.base_width < 0:
            self.x2 = self.x1 + self.base_width

    def draw(self, win):
        win.blit(self.image, (self.x1, self.y))
        win.blit(self.image, (self.x2, self.y))


def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def draw_window(win, birds, pipes, base, score, gen, pipe_index, learn_again_button, load_model_button, save_model_button):
    if gen == 0:
        gen = 1
    win.blit(bg_image, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    for bird in birds:
        bird.draw(win)

    score_label = score_font.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (width - score_label.get_width() - 15, 10))

    score_label = score_font.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    score_label = score_font.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.draw.rect(win, (200,200,200), learn_again_button)
    learn_again_text = button_font.render("Learn Again", 1, (0,0,0))
    text_rect = learn_again_text.get_rect(center=learn_again_button.center)
    win.blit(learn_again_text, text_rect.topleft)

    pygame.draw.rect(win, (200,200,200), load_model_button)
    load_model_text = button_font.render("Load Model", 1, (0,0,0))
    text_rect = load_model_text.get_rect(center=load_model_button.center)
    win.blit(load_model_text, text_rect.topleft)

    pygame.draw.rect(win, (200,200,200), save_model_button)
    save_model_text = button_font.render("Save Model", 1, (0,0,0))
    text_rect = save_model_text.get_rect(center=save_model_button.center)
    win.blit(save_model_text, text_rect.topleft)

    pygame.display.update()



########################################################################################################
########################################################################################################
# our code start here
########################################################################################################
########################################################################################################


def eval_genomes(genomes, config):
    global screen, gen

    learn_again_button = pygame.Rect(width - 200 - 10, height - 150, 200, 40)
    load_model_button = pygame.Rect(width - 200 - 10, height - 100, 200, 40)
    save_model_button = pygame.Rect(width - 200 - 10, height - 50, 200, 40)

    win = screen
    gen += 1

    nets = []
    birds = []
    genomes_list = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        genomes_list.append(genome)

    base = Base(floor_y)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if learn_again_button.collidepoint(mouse_pos):
                    return True
                if load_model_button.collidepoint(mouse_pos):
                    try:
                        with open("best.model", "rb") as f:
                            model = pickle.load(f)
                        play_loaded_model(model, config)
                        return False
                    except FileNotFoundError:
                        print("best.model not found. Train model first.")
                        return False
                if save_model_button.collidepoint(mouse_pos):
                    if nets:
                        pickle.dump(nets[0], open("best.model", "wb"))
                        print("Current model saved to best.model")
                    else:
                        print("No model to save yet.")


        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipe_top_img.get_width():
                pipe_index = 1

        for x, bird in enumerate(birds):
            genomes_list[x].fitness += 0.1
            bird.move()

            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            if output[0] > 0.5:
                bird.jump()

        base.move()

        removed_pipes = []
        add_new_pipe = False
        for pipe in pipes:
            pipe.move()
            for bird in birds:
                if pipe.collide(bird, win):
                    genomes_list[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    genomes_list.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.pipe_top_img.get_width() < 0:
                removed_pipes.append(pipe)

            if not pipe.has_passed and pipe.x < bird.x:
                pipe.has_passed = True
                add_new_pipe = True

        if add_new_pipe:
            score += 1
            for genome in genomes_list:
                genome.fitness += 5
            pipes.append(Pipe(width))

        for pipe_remove in removed_pipes:
            pipes.remove(pipe_remove)

        for bird in birds:
            if bird.y + bird.image.get_height() - 10 >= floor_y or bird.y < -50:
                nets.pop(birds.index(bird))
                genomes_list.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        learn_again_button = pygame.Rect(width - 200 - 10, height - 150, 200, 40)
        load_model_button = pygame.Rect(width - 200 - 10, height - 100, 200, 40)
        save_model_button = pygame.Rect(width - 200 - 10, height - 50, 200, 40)
        draw_window(screen, birds, pipes, base, score, gen, pipe_index, learn_again_button, load_model_button, save_model_button)

        if score > 100:
            pickle.dump(nets[0],open("best.model", "wb"))
            return False
    return False


def play_loaded_model(model, config):
    global screen
    win = screen

    bird = Bird(230,350)
    base = Base(floor_y)
    pipes = [Pipe(700)]
    score = 0
    gen = 1
    pipe_index = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        pipe_index = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].pipe_top_img.get_width():
            pipe_index = 1

        bird.move()
        output = model.activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))
        if output[0] > 0.5:
            bird.jump()

        base.move()

        add_new_pipe = False
        removed_pipes = []
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird, win):
                pipes = [Pipe(700)]
                score = 0
                bird = Bird(230,350)
                base = Base(floor_y)
                break

            if pipe.x + pipe.pipe_top_img.get_width() < 0:
                removed_pipes.append(pipe)

            if not pipe.has_passed and pipe.x < bird.x:
                pipe.has_passed = True
                add_new_pipe = True

        if add_new_pipe:
            score += 1
            pipes.append(Pipe(width))

        for pipe_remove in removed_pipes:
            pipes.remove(pipe_remove)

        if bird.y + bird.image.get_height() - 10 >= floor_y or bird.y < -50:
            pipes = [Pipe(700)]
            score = 0
            bird = Bird(230,350)
            base = Base(floor_y)


        learn_again_button = pygame.Rect(width - 200 - 10, height - 150, 200, 40)
        load_model_button = pygame.Rect(width - 200 - 10, height - 100, 200, 40)
        save_model_button = pygame.Rect(width - 200 - 10, height - 50, 200, 40)
        draw_window(screen, [bird], pipes, base, score, gen, pipe_index, learn_again_button, load_model_button, save_model_button)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    while True:
        population = neat.Population(config)

        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        #population.add_reporter(neat.Checkpointer(5))

        learn_again = population.run(eval_genomes, 50)

        if not learn_again:
            continue


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
    
############################################################################################
############################################################################################
# End of our code
############################################################################################
############################################################################################