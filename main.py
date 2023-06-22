import pygame
import pygame_widgets
import random
import time
import sys

from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown

list_of_bars = []  # [rect, rgb]
num_of_bars = 0
running = True
screen = None
clock = None
size_slider = None
shuffle_button = None
size_slider_output = None
algo_dropdown = None
start_button = None
descending_button = None


def main():

    global screen
    global clock
    global size_slider
    global shuffle_button
    global running
    global list_of_bars  # All the bars (rectangles)
    global num_of_bars  # Number of bars
    global size_slider_output
    global algo_dropdown
    global start_button
    global descending_button

    pygame.init()
    pygame.display.set_caption('Sort Visualizer')
    screen = pygame.display.set_mode((700, 450))
    clock = pygame.time.Clock()

    # ----------------------------------------------------------------------------------------------------------------

    size_slider = Slider(screen, 50, 30, 100, 10, min=10, max=200, step=1)
    shuffle_button = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        430,  # X-coordinate of top left corner
        15,  # Y-coordinate of top left corner
        120,  # Width
        30,  # Height

        # Optional Parameters
        text='Shuffle',  # Text to display
        fontSize=20,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(100, 100, 100),  # Colour of button when not being interacted with
        hoverColour=(150, 150, 150),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        onClick=fisher_yates_shuffle  # Function to call when clicked on
    )
    descending_button = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        430,  # X-coordinate of top left corner
        55,  # Y-coordinate of top left corner
        120,  # Width
        30,  # Height

        # Optional Parameters
        text='Descending Order',  # Text to display
        fontSize=20,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(100, 100, 100),  # Colour of button when not being interacted with
        hoverColour=(150, 150, 150),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        onClick=create_bars_descending  # Function to call when clicked on
    )
    size_slider_output = TextBox(screen, 28, 60, 145, 25, fontSize=20)
    size_slider_output.disable()  # Act as label instead of textbox
    algo_dropdown = Dropdown(
        screen, 200, 10, 170, 30, name='Select Sorting Algorithm',
        choices=[
            'Bubble Sort',
            'Insertion Sort',
            'Selection Sort',
            'Merge sort',
            'Quicksort'
        ],
        borderRadius=3,
        inactiveColour=(100, 100, 100),  # Colour of button when not being interacted with
        hoverColour=(150, 150, 150),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        values=['B', 'I', 'S', 'M', 'Q'],
        direction='down',
        textHAlign='left'
    )
    start_button = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        575,  # X-coordinate of top left corner
        25,  # Y-coordinate of top left corner
        100,  # Width
        50,  # Height

        # Optional Parameters
        text='Start',  # Text to display
        fontSize=20,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(100, 100, 100),  # Colour of button when not being interacted with
        hoverColour=(150, 150, 150),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        onClick=run_algorithm  # Function to call when clicked on
    )

    # ----------------------------------------------------------------------------------------------------------------

    while running:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        pygame_widgets.update(events)
        update_num_of_bars = size_slider.getValue()  # Get the number of bars from the slider

        if num_of_bars != update_num_of_bars:
            create_bars(update_num_of_bars)  # Create a new list of bars

        display()

    pygame.quit()


def exiting():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def run_algorithm():

    global algo_dropdown

    algo = algo_dropdown.getSelected()

    if algo == 'B':
        bubble_sort()
    elif algo == 'I':
        insertion_sort()
    elif algo == 'S':
        selection_sort()
    elif algo == 'M':
        merge_sort()
    elif algo == 'Q':
        quicksort()
    else:
        print("None")


def bubble_sort():

    global list_of_bars

    n = len(list_of_bars)

    while True:
        swapped = False
        for i in range(1, n):

            x1, y1, w1, h1 = list_of_bars[i-1][0]
            x2, y2, w2, h2 = list_of_bars[i][0]

            list_of_bars[i-1] = [pygame.Rect(x1, y1, w1, h1), (255, 0, 0)]
            display()
            exiting()
            list_of_bars[i-1] = [pygame.Rect(x1, y1, w1, h1), (255, 255, 255)]

            if h1 > h2:
                list_of_bars[i] = [pygame.Rect(x2, y1, w1, h1), (255, 255, 255)]
                list_of_bars[i-1] = [pygame.Rect(x1, y2, w2, h2), (255, 255, 255)]
                swapped = True

        n = n - 1
        if not swapped:
            break

    for i in range(len(list_of_bars)):
        x, y, w, h = list_of_bars[i][0]
        list_of_bars[i] = [pygame.Rect(x, y, w, h), (0, 255, 0)]
        display()


def insertion_sort():

    global list_of_bars

    n = len(list_of_bars)

    i = 1
    while i < n:

        j = i

        # To display
        x1, y1, w1, h1 = list_of_bars[j][0]
        list_of_bars[j] = [pygame.Rect(x1, y1, w1, h1), (255, 0, 0)]
        display()
        exiting()
        list_of_bars[j] = [pygame.Rect(x1, y1, w1, h1), (255, 255, 255)]

        while j > 0 and list_of_bars[j-1][0][3] > list_of_bars[j][0][3]:

            x1, y1, w1, h1 = list_of_bars[j-1][0]
            x2, y2, w2, h2 = list_of_bars[j][0]

            # To display
            list_of_bars[j] = [pygame.Rect(x1, y1, w1, h1), (255, 0, 0)]
            display()
            exiting()
            list_of_bars[j] = [pygame.Rect(x1, y1, w1, h1), (255, 255, 255)]

            list_of_bars[j] = [pygame.Rect(x2, y1, w1, h1), (255, 255, 255)]
            list_of_bars[j - 1] = [pygame.Rect(x1, y2, w2, h2), (255, 255, 255)]
            j = j - 1

        i = i + 1

    for i in range(len(list_of_bars)):
        x, y, w, h = list_of_bars[i][0]
        list_of_bars[i] = [pygame.Rect(x, y, w, h), (0, 255, 0)]
        display()


def selection_sort():

    global list_of_bars

    n = len(list_of_bars)

    for i in range(0, n-1):

        exiting()

        xi, yi, wi, hi = list_of_bars[i][0]
        list_of_bars[i] = [pygame.Rect(xi, yi, wi, hi), (255, 0, 0)]
        display()

        j_min = i
        for j in range(i+1, n):

            exiting()

            xj, yj, wj, hj = list_of_bars[j][0]
            list_of_bars[j] = [pygame.Rect(xj, yj, wj, hj), (5, 124, 252)]
            display()
            list_of_bars[j] = [pygame.Rect(xj, yj, wj, hj), (255, 255, 255)]

            if list_of_bars[j][0][3] < list_of_bars[j_min][0][3]:

                if j_min != i:
                    x, y, w, h = list_of_bars[j_min][0]
                    list_of_bars[j_min] = [pygame.Rect(x, y, w, h), (255, 255, 255)]

                j_min = j

                x, y, w, h = list_of_bars[j_min][0]
                list_of_bars[j_min] = [pygame.Rect(x, y, w, h), (0, 255, 0)]
                display()
                exiting()

        if j_min != i:
            x1, y1, w1, h1 = list_of_bars[i][0]
            x2, y2, w2, h2 = list_of_bars[j_min][0]
            list_of_bars[j_min] = [pygame.Rect(x2, y1, w1, h1), (255, 255, 255)]
            list_of_bars[i] = [pygame.Rect(x1, y2, w2, h2), (255, 255, 255)]
        else:
            list_of_bars[i] = [pygame.Rect(xi, yi, wi, hi), (255, 255, 255)]

    for i in range(len(list_of_bars)):
        x, y, w, h = list_of_bars[i][0]
        list_of_bars[i] = [pygame.Rect(x, y, w, h), (0, 255, 0)]
        display()


def merge_sort():

    global list_of_bars
    n = len(list_of_bars)

    def split(start, end):

        exiting()

        # One element
        if start + 1 == end:
            return

        # Get mid index
        mid = (start + end) // 2

        # Split
        split(start, mid)
        split(mid, end)

        # Merge
        merge(start, mid, end)

        for index in range(start, end):
            exiting()
            list_of_bars[index] = [list_of_bars[index][0], (255, 0, 0)]
            display()

        for index in range(start, end):
            list_of_bars[index] = [list_of_bars[index][0], (255, 255, 255)]

    # Left sorted portion: [start, mid-1]
    # Right sorted portion: [mid, end-1]
    def merge(start, mid, end):

        global list_of_bars

        left = list_of_bars[start:mid]
        right = list_of_bars[mid:end]

        x_cord = []
        for b in left:
            x_cord.append(b[0][0])
        for b in right:
            x_cord.append(b[0][0])
        x_cord.sort()

        temp = []

        l = 0
        r = 0

        while l < len(left) and r < len(right):
            exiting()
            if left[l][0][3] < right[r][0][3]:
                left[l][0][0] = x_cord[0]
                x_cord.pop(0)
                temp.append(left[l])
                l = l + 1
            else:
                right[r][0][0] = x_cord[0]
                x_cord.pop(0)
                temp.append(right[r])
                r = r + 1

        if l < len(left):
            exiting()
            while l < len(left):
                left[l][0][0] = x_cord[0]
                x_cord.pop(0)
                temp.append(left[l])
                l = l + 1

        if r < len(right):
            exiting()
            while r < len(right):
                right[r][0][0] = x_cord[0]
                x_cord.pop(0)
                temp.append(right[r])
                r = r + 1

        list_of_bars[start:end] = temp

    split(0, n)

    for i in range(len(list_of_bars)):
        x, y, w, h = list_of_bars[i][0]
        list_of_bars[i] = [pygame.Rect(x, y, w, h), (0, 255, 0)]
        display()


def quicksort():

    global list_of_bars
    n = len(list_of_bars)

    def quick_sort(l, r):
        if l < r:
            p = partition(l, r)
            quick_sort(l, p-1)
            quick_sort(p+1, r)

    def partition(l, r):

        mid = (l+r) // 2  # pivot

        list_of_bars[l][1] = (255, 0, 0)  # left
        list_of_bars[mid][1] = (0, 255, 0)  # pivot
        list_of_bars[r][1] = (0, 0, 255)  # right
        display()
        time.sleep(0.5)

        list_of_bars[r][0][0], list_of_bars[mid][0][0] = list_of_bars[mid][0][0], list_of_bars[r][0][0]
        list_of_bars[r], list_of_bars[mid] = list_of_bars[mid], list_of_bars[r]

        pivot = list_of_bars[r][0][3]

        for i in range(l, r):

            exiting()
            display()

            if list_of_bars[i][0][3] < pivot:
                list_of_bars[i][0][0], list_of_bars[l][0][0] = list_of_bars[l][0][0], list_of_bars[i][0][0]
                list_of_bars[i], list_of_bars[l] = list_of_bars[l], list_of_bars[i]
                l = l + 1

        list_of_bars[l][0][0], list_of_bars[r][0][0] = list_of_bars[r][0][0], list_of_bars[l][0][0]
        list_of_bars[l], list_of_bars[r] = list_of_bars[r], list_of_bars[l]

        for i in range(n):
            list_of_bars[i][1] = (255, 255, 255)

        return l  # pivot index

    quick_sort(0, n-1)

    for k in range(len(list_of_bars)):
        x, y, w, h = list_of_bars[k][0]
        list_of_bars[k] = [pygame.Rect(x, y, w, h), (0, 255, 0)]
        display()


def create_bars_descending():

    global num_of_bars
    global list_of_bars

    list_of_bars = []

    for i in range(num_of_bars):
        bar_width = 700 / num_of_bars

        width = bar_width - 2
        height = 350 + ((10 - 350) / (num_of_bars - 1 - 0)) * (i - 0)
        left = bar_width * i + 1
        top = 100 + (350 - height)

        list_of_bars.append([pygame.Rect(left, top, width, height), (255, 255, 255)])


def display():

    global screen
    global list_of_bars
    global clock
    global size_slider_output
    global size_slider

    screen.fill((0, 0, 0))

    canvas = pygame.Surface((700, 450))

    top_camera = pygame.Rect(0, 0, 700, 100)
    bottom_camera = pygame.Rect(0, 100, 700, 350)

    canvas.fill((34, 71, 153), top_camera)
    canvas.fill((50, 50, 50), bottom_camera)

    screen.blit(canvas, (0, 0), top_camera)
    screen.blit(canvas, (0, 100), bottom_camera)

    for b in list_of_bars:
        bar = b[0]
        rgb = b[1]
        pygame.draw.rect(screen, rgb, bar)

    events = pygame.event.get()

    size_slider_output.setText("Number of bars:  " + str(size_slider.getValue()))
    pygame_widgets.update(events)

    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)


def create_bars(update_num_of_bars):

    global num_of_bars
    global list_of_bars

    num_of_bars = update_num_of_bars
    list_of_bars = []

    for i in range(num_of_bars):
        bar_width = 700 / num_of_bars

        width = bar_width - 2
        height = 10 + ((350 - 10) / (num_of_bars - 1 - 0)) * (i - 0)
        left = bar_width * i + 1
        top = 100 + (350 - height)

        list_of_bars.append([pygame.Rect(left, top, width, height), (255, 255, 255)])


def fisher_yates_shuffle():

    global list_of_bars

    random.seed(time.time())

    for i in range(len(list_of_bars)-1, 0, -1):

        exiting()

        j = random.randint(0, i)

        x1, y1, w1, h1 = list_of_bars[i][0]
        x2, y2, w2, h2 = list_of_bars[j][0]

        list_of_bars[j] = [pygame.Rect(x2, y1, w1, h1), (255, 0, 0)]
        list_of_bars[i] = [pygame.Rect(x1, y2, w2, h2), (255, 0, 0)]

        display()

        list_of_bars[j] = [pygame.Rect(x2, y1, w1, h1), (255, 255, 255)]
        list_of_bars[i] = [pygame.Rect(x1, y2, w2, h2), (255, 255, 255)]

        time.sleep(0.05)


if __name__ == "__main__":
    main()
