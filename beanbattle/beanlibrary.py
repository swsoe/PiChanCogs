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
        
        beans.append(Bean("Ad-Sponsored", 4, 0, (0,255,0)))
        beans.append(Bean("Blessed", 7, 0,(255,255,0)))
        beans.append(Bean("Cursed", 6, 0,(166,77,121)))
        beans.append(Bean("Degenerate", 3, 0,(102,102,102)))
        beans.append(Bean("Elemental", 8, 0,(255,153,0)))
        beans.append(Bean("Fabled", 18, 0,(180,95,6)))
        beans.append(Bean("Ghostly", 16, 0,(207,226,243)))
        beans.append(Bean("Harmless", 1, 0,(164,194,244)))
        beans.append(Bean("**ILLEGAL**", 11, 0,(0,0,255)))
        beans.append(Bean("Jinxed", 13, 0,(255,0,255)))
        beans.append(Bean("Killer", 19, 0,(204,0,0)))
        beans.append(Bean("*Liberal*", 14, 0,(255,0,0)))
        beans.append(Bean("Magical", 15, 0,(153,0,255)))
        beans.append(Bean("Nimble", 10, 0,(74,134,232)))
        beans.append(Bean("Ornery", 5, 0,(106,168,79)))
        beans.append(Bean("Parasitic", 9, 0,(152,0,0)))
        beans.append(Bean("~~[Redacted]~~", 21, 0,(153,153,153)))
        beans.append(Bean(":sparkles:**S E C R E T**:sparkles:", datetime.datetime.now().hour, 0,(241, 194, 50))) #Current hour (24HR format)
        beans.append(Bean("Tiny", 2, 0,(0, 255, 255)))
        beans.append(Bean("**Ultimate**", 20, 0,(255,255,255)))
        beans.append(Bean("Vampire", 17, 0,(103,78,167)))
        beans.append(Bean("**W**i*L*d & W**a**C*k*Y", random.randint(1,20), 0,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))) #Random int 1-20
        beans.append(Bean("XII", 12, 0,(69,129,142)))
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