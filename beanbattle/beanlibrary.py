import random
import datetime

class Bean(object):

    def __init__(self, name: str, ac: int, coins: int, color):
        self.name = name
        self.ac = ac
        self.coins = coins
        self.color = color

class BeanLibrary:

    def GetBeans():
        beans = []
        
        beans.append(Bean("Ad-Sponsored", 4, 30, (0,255,0)))
        beans.append(Bean("Blessed", 7, random.randint(5,7),(255,255,0)))
        beans.append(Bean("Cursed", 6, random.randint(4,6),(166,77,121)))
        beans.append(Bean("Degenerate", 3, random.randint(2,4),(102,102,102)))
        beans.append(Bean("Elemental", 8, random.randint(6,8),(255,153,0)))
        beans.append(Bean("Fabled", 18, 20,(180,95,6)))
        beans.append(Bean("Ghostly", 16, random.randint(18,19),(207,226,243)))
        beans.append(Bean("Harmless", 1, 1,(164,194,244)))
        beans.append(Bean("**ILLEGAL**", 11, random.randint(12,13),(0,0,255)))
        beans.append(Bean("Jinxed", 13, 0,(255,0,255)))
        beans.append(Bean("Killer", 19, 20,(204,0,0)))
        beans.append(Bean("*Liberal*", 14, random.randint(14,15),(255,0,0)))
        beans.append(Bean("Magical", 15, random.randint(16,17),(153,0,255)))
        beans.append(Bean("Nimble", 10, random.randint(10,11),(74,134,232)))
        beans.append(Bean("Ornery", 5, random.randint(3,5),(106,168,79)))
        beans.append(Bean("Parasitic", 9, random.randint(7,9),(152,0,0)))
        beans.append(Bean("~~[Redacted]~~", 21, -5,(153,153,153)))
        beans.append(Bean(":sparkles:**S E C R E T**:sparkles:", datetime.datetime.now().hour, 50,(241, 194, 50)))
        beans.append(Bean("Tiny", 2, random.randint(1,3),(0, 255, 255)))
        beans.append(Bean("**Ultimate**", 20, 100,(255,255,255)))
        beans.append(Bean("Vampire", 17, datetime.datetime.now().hour,(103,78,167)))
        beans.append(Bean("**W**i*L*d & W**a**C*k*Y", random.randint(1,20), random.randint(1,20),(random.randint(0,255),random.randint(0,255),random.randint(0,255))))
        beans.append(Bean("XII", 12, 12,(12,120,120)))
        return beans
    
    def GetDefeatedMessage():
        return [
            "The {beanName} Bean calls the police! {userName} is under arrest!! Off to Gay Baby Jail you go!",
            "{userName} misses the attack! The {beanName} Bean manages to get away!",
            "{userName} tries to take aim, but doesn’t have the guts to pull the trigger...",
            "{userName} drops the gun and shoots themself in the foot! {userName} takes "+str(random.randint(1,12))+" damage!",
            "{userName} attacks! The shot hits the floor and scares the {beanName} Bean away!",
            "{userName} attempts to the corner the {beanName} Bean. It draws a gun of its own and fires! {userName} blacks out!!",
            "The {beanName} Bean counters the attack! {userName} takes "+str(random.randint(1,99))+" damage!!! Ouch!",
            "The {beanName} Bean instantly dematerializes!",
            "The {beanName} Bean begs for its life! As {userName} lowers their gun, the bean escapes!",
            "The {beanName} Bean has already defeated you. {userName}’s head explodes!!!"
        ]