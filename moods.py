from PIL import Image, ImageDraw, ImageFont
import datetime


def draw_block(start, difference, moods):
    daily_moods = []  # list of moods (no repeats)
    mood_count = {}  # count of each mood
    highest = 0  # highest count of a mood

    for mood in moods:  # just sorts through the day's moods for above vars
        if mood not in daily_moods:
            daily_moods.append(mood)
            mood_count[mood] = moods.count(mood)
            if moods.count(mood) > highest:
                highest = moods.count(mood)

    daily_moods = sorted(daily_moods)  # alpha sort so the bars have some order

    increment = difference / len(daily_moods)  # separation of bars
    coord_list = [[start]]  # beginning left coord of box

    for i in range(len(daily_moods)):  # makes list of x coords between all increments and y displacement
        lower_x = start + (increment * (i + 1))
        y_coord = (1 - (mood_count[daily_moods[i]] / highest)) * 93
        coord_list.append([lower_x, y_coord])

    return coord_list, daily_moods


def weekly_moods(moods: list, uuid: int):
    # defines colours of bars (missing 'confident': 'orange', 'tentative': 'green', 'analytical': 'pink')
    colours = {
        'anger': (251, 105, 98),
        'fear': (168, 228, 239),
        'joy': (252, 252, 153),
        'sadness': (121, 222, 121)
    }
    lower = 260  # lower is the bottom coord of bar, upper is top but it changes
    upper = 167
    difference = 93  # difference between the 2 sides of the boxes
    blocks = [857, 722, 586, 450, 313, 176, 44]  # left coord of each box

    back = Image.open("resource/grey_back.png")  # grey background with the boxes
    back_draw = ImageDraw.Draw(back)

    for i in range(len(blocks)):
        if len(moods[i]) != 0:
            coords, daily_moods = draw_block(blocks[i], difference, moods[i])  # for each box, the function is called

            for j in range(len(daily_moods)):
                back_draw.rectangle((coords[j][0] + 1, upper + coords[j + 1][1], coords[j + 1][0], lower),
                                    fill=colours[daily_moods[j]])  # draws each mood for each box

    #  date text
    today = datetime.datetime.now().date()
    initial_coord = 860
    difference = 134
    scale = 1.2
    font = ImageFont.truetype("resource/Roboto-Regular.ttf", 17)

    for i in range(7):
        back_draw.text((initial_coord - (difference * i) - (i * scale), 270), (today - datetime.timedelta(i + 1)
                                                                               ).strftime('%m/%d/%Y'),
                       fill=(119, 131, 211), font=font)

    back.save(f"process/{uuid}.png")
