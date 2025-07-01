import random


class PlaybackError(Exception):
    """Raised for any recoverable playback-related failure."""


class HumanError(Exception):
    """Raised when the user makes an invalid request."""


HUMAN_ERROR_TITLES = [
    # 🇩🇪 Deutsch – Lustig & allgemein
    "Hoppla, Knecht hat’s vermasselt!",
    "Das war wohl nix, Kollege!",
    "Oh mei, da is was schiefglaufen!",
    "Schlaubi-Schlumpf war heute wohl krank.",
    "Kaputt, aber mit Stil!",
    "So war das nicht geplant, Chef!",
    "Irgendwas is’ immer!",
    "Glänzend gescheitert!",
    "Na bravo, wieder ein Griff ins Klo.",
    "Alles futschikato!",
    "Hossa, der Fehlerteufel war da!",
    "Mit Anlauf ins Fettnäpfchen!",
    "Einmal dumm geklickt, bitte!",
    "Tja, da hat jemand gepennt.",
    "Voll verkackt – aber charmant!",
    "Mensch ärgere dich nicht… zu spät!",
    "Da hat der Praktikant wohl wieder Code geschrieben!",
    "Heut is’ net dein Tag, gell?",
    "Hirn.exe wurde unerwartet beendet.",
    "Zonk! Kein Gewinn heut.",
    "Leider geil, aber leider falsch.",
    "Einmal mit Profis…",
    "Schon wieder 4711 auf dem Kessel!",
    "Das war’s mit der Effizienz.",
    "Warum einfach, wenn’s auch nicht geht?",

    # 🇩🇪 Deutsch – Norddeutsch / Platt / Schnack
    "Wat mutt, dat mutt – aber nich’ so!",
    "Dat geiht so nich, mien Jung!",
    "Na, dat is mol’n dösbaddeliger Klick!",
    "Allens in’n Eimer!",
    "Da is wat in’n Teich jefallen.",
    "Nu is’ auch egal, oder wat?",
    "Jo, dat hätt auch nich schlechter laufen künnt.",
    "Haste schön vergeigt, ne?",
    "Da hat der Klabautermann wieder mitgemischt!",
    "Is wie Ebbe – da fehlt wat.",

    # 🇩🇪 Deutsch – Sächsisch
    "Nu gugge ma – alles im Eimer!",
    "Hach nee, das war nüschd!",
    "Da hättste ooch druff kommen könn!",
    "Bissl viel Risiko für keen Plan, oder?",
    "Na, da is de Technik wohl aus’m Bett gefallen.",
    "Haste schön verbockt, Kumpel!",
    "So wird das nüschd mit de Weltrevolution.",
    "Ich sach’s dir: Der Klick war sächsisch daneben.",
    "Das war wie Bratwurst im Toaster – klingt gut, geht schief.",
    "Oweh… de Software is nimmer ganz frisch.",

    # 🇩🇪 Deutsch – Hochdeutsch flach & trocken
    "Das Ergebnis war... ambitioniert.",
    "Unerwartete Klickfreude erkannt.",
    "Irgendwas ist immer kaputt.",
    "Bediener sitzt zu nah am Gerät.",
    "Fehler gefunden – Ursache unklar.",
    "Das war vermutlich Absicht… oder?",
    "Schön gedacht, schlecht gemacht.",
    "Mission: Unmöglich (ausgeführt).",
    "War das jetzt Ironie oder ernst gemeint?",
    "Berechnung abgebrochen – Mitleid geladen.",

    # 🇬🇧 English – Funny
    "Oopsie daisy!",
    "Who let the bugs out?",
    "Well, that escalated quickly!",
    "Congratulations! You broke it.",
    "Ah, classic user move!",
    "That's a paddlin’.",
    "Keyboard not found… Press any key.",
    "You tried. A+ for effort!",
    "It’s not a bug, it’s a surprise feature.",
    "Ruh-roh, Raggy!",
    "Someone needs more coffee.",
    "Oof, that’s gonna leave a mark.",
    "Abort mission, Captain!",
    "Good job, intern!",
    "That’s what she *didn’t* say.",
    "You pressed the forbidden button.",
    "Houston, we have a you.",
    "The gods of code are not amused.",
    "Error 418: I'm a teapot.",
    "Big brain moment™",
    "And just like that... poof.",
    "You had one job!",
    "Glitch gremlins strike again!",
    "Close, but nope.",
    "Well, butter my biscuit!",

    # 🇬🇧 English – More
    "System went full potato.",
    "This is why we can’t have nice things.",
    "Error 404: Common Sense Not Found.",
    "You’ve officially confused the server.",
    "Well, crap.",
    "It broke itself. Promise.",
    "The matrix glitched. Blame Neo.",
    "Magic smoke has escaped.",
    "Look, a shiny error!",
    "The code elves are on strike.",
    "This action requires a brain.",
    "Whoops, spaghetti code moment.",
    "You summoned the wrong function.",
    "Guess we’re winging it now!",
    "That wasn’t supposed to happen™",
    "Oops… We did it again!",
    "Something went wrong. Obviously.",
    "Expectation: Genius. Reality: Nope.",
    "Broken like Monday morning.",
    "Well, paint me green and call me a bug.",
    "Epic fail detected.",
    "Press F to pay respects.",
    "Please consult your nearest wizard.",
    "Warning: Sarcasm module overloaded.",
    "User input rated “legendary fail”."
]


def get_random_human_error_title() -> str:
    return random.choice(HUMAN_ERROR_TITLES)
