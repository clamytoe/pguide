# pguide
> Parental Guide assistant for media that uses IMDb.

My kids are big movie and anime buffs and are constantly asking me to look up shows to see if they are allowed to watch them. This of course takes time, more so when they bring you a list of them! I wrote this script to help me out with that task.

I was surprised to discover that it also worked for video games!

## How to set it all up
First of all, you have to setup the environment. I've included both a *requirements.txt* and an *environment.yml* file in order to make things easier. Perform the steps in the *Initial setup* and *Final setup* but do either the *Anaconda* or *Python* one depending on which one you have installed on your system.

#### Initial setup
```bash
cd Projects
git clone https://github.com/clamytoe/pguide.git
cd pguide
```

#### Anaconda setup
```bash
conda env create
```

#### Regular Python setup
```bash
pip install -r requirements.txt
```

#### Final setup
```bash
activate pguide # or source activate pguide
pip install git+https://github.com/alberanid/imdbpy
```

## How to run
Once that's all out of the way simple run the program and follow the prompts.

```bash
python pguide.py
```

## Sample run
```bash
What movie/show would you like me to look up for you? attack on titan
Please wait while I search for "attack on titan"...
Found 20 matches.
[0] "Attack on Titan" (2013)
[1] Attack on Titan (in development) (None)
[2] "Read Right to Left" Attack on Titan (2013)
[3] Attack on Titan: Part 1 (2015)
[4] Attack on Titan: Part 2 (2015)
[5] "Attack on Titan: Junior High" (2015)
[6] Attack on Titan Crimson Bow and Arrow (2014)
[7] Attack on Titan: The Wings of Freedom (2015)
[8] Attack on Titan Abridged (2013)
[9] "Nerdy Nummies" Attack on Titan Tarts (2016)
[10] "Gaming" Attack on Titan (2016)
[11] "Attack, The" Attack's Attack on Titan (2017)
[12] "Philosophy of, The" Attack on Titan (2017)
[13] "Yo Reviews" Attack on Titan 2x01 (2017)
[14] "JesuOtaku Anime Reviews" Attack on Titan: Part 1 (2014)
[15] Attack on Titan: Counter Rockets (2015)
[16] Attack on Titan: Wings of Freedom (2016) (VG)
[17] "AfterBuzz TV's Spotlight On" Attack on Titan Interview (2015)
[18] Attack on Titan: Humanity in Chains (2014) (VG)
[19] "Film Theory" DON'T Attack the Titans! (Attack on Titan) (2016)
Which one would you like to review? 0
Retrieving additional information for ""Attack on Titan" (2013)"
[PLOT]
 After his hometown is destroyed and his mother is killed, young Eren Yeager vows to cleanse the earth of the giant humanoid Titans that have brought humanity to the brink of extinction.
[RATINGS]
 United States:TV-14  United States:TV-MA
[NUDITY]
 2 of 6 found this moderate
  * 3/10
  * Titans, the main antagonists, are giant humanoid creatures, mostly of male physiology, always shown naked but they have NO sexual or digestive organs so there's nothing truly offensive. The only female of the species is skinless, so besides not having any genitalia like all the others, she has no nipples either.
Would you like to review a different one? [y/n]n
Ok
```
