'''
So, we'll need to use OOP for discord roles. Some variables include:
time spent chatting(in minutes,daily), vote boosting, person's current level, current xp, desired level.
time spent CHATTING in VC(in minutes,weekly)
'''
"""
To create a server profile with fully customized settings, do the following:

server_default_settings = Settings("linear" , 1 , None , True , False) #create default settings 
server_XP_settings = XPSettings(15,40,60) #create message xp settings
server_voice_settings = VoiceXP(15,60,180,3) #create voice xp settings
lvlrole2 = LevelRole('lvlrole2',0,2), #create second level role
etc. #and continue until all your roles are created
level_role_list = [lvlrole1,lvlrole2,etc...] #add them to a list

nonlvlrole1 = NonLevelRole('nonlvlrole1',0) #do the same for any non-level roles
etc. 
non_level_role_list = [nonlvlrole1,etc.] #add them to a list
server = Server(server_default_settings,server_XP_settings,server_voice_settings,
                level_role_list,non_level_role_list) #create the server object

you then only need to get the right information about the user and then create the user
user = User(60,0,0,60,0,False)
Run these three to get results:
- user.target_xp(server)
- time_sum = user.message_xp_time(server) #time sum in days
- output_result_string = user.display_time_estimate(time_sum,server)
the output is a formatted string. For more control over the output, please get the values from
user.calculate_time_estimate(server) instead

time sum is the main estimate, while the min are weaker, more general estimates.
"""


class Settings:
    def __init__(self,curve = 'Linear',multiplier = 1, max_level = float('inf'),stack_rewards = True,stack_boosters = False):
        self.curve = curve
        self.multiplier = multiplier
        self.max_level = max_level
        self.stack_rewards = stack_rewards
        self.stack_boosters = stack_boosters

class XPSettings:
    def __init__(self,min_xp,max_xp,cooldown):
        self.min_xp = min_xp
        self.max_xp = max_xp
        self.cooldown = cooldown #in seconds

class VoiceXP(XPSettings):
    def __init__(self,min_xp,max_xp,cooldown,min_members):
        super().__init__(min_xp,max_xp,cooldown)
        self.min_members = min_members
        self.voice = True
    


class Role: #We need a role class since arcane allows some role to have xp boosts and so can take them into consideration for a more accurate result

    Level_roles = [] #list of roles which are given at specific levels
    Non_level_roles = [] #list of roles which are not given at specific levels but provide an xp boost

    def __init__(self, rolename:str, xpboost:float):
        self.rolename = rolename #name of the role in the server
        self.xpboost = xpboost #xp boost in decimal(10%=0.1)

    @property
    def get_name(self): #method to obtain the name of the role
        return self.rolename
    
    @property
    def get_boost(self): #method to obtain the role's xp boost
        return self.xpboost
    
    def get_all(self): #method to obtain all the role's attributes
        return self.rolename, self.xpboost

    @staticmethod
    def empty_lists(): #method to empty the level and non-level role lists
        Role.Level_roles = []
        Role.Non_level_roles = []

    @staticmethod #adapted for the role
    def find_largest_boost(role_list):
        #this function finds the largest role boost in a list of role objects
        if not role_list:  # Handle empty list case
            return 0
        
        largest_so_far = role_list[0].xpboost  # Assume the first element is the largest initially
        for role in role_list:
            if role.xpboost > largest_so_far:
                largest_so_far = role.xpboost
        return largest_so_far
    
    def __str__(self):
        return f'{self.rolename}'

class LevelRole(Role):
    def __init__(self,rolename:str, xpboost:float, levelgranted:int):
        super().__init__(rolename,xpboost)
        self.levelgranted = levelgranted #level at which the role is given
        Role.Level_roles.append(self) #add the role to the level roles list

    @property
    def get_level(self): #method to obtain the level at which the role is given
        return self.levelgranted
    
    def get_all(self): #method to obtain all the role's attributes
        return self.rolename,self.xpboost,self.levelgranted
    
class NonLevelRole(Role):
    def __init__(self,rolename:str,xpboost:float):
        super().__init__(rolename,xpboost)
        Role.Non_level_roles.append(self) #add the role to the non-level roles list



class Server:
    def __init__(self, def_settings:Settings=None, message_settings:XPSettings=None, voice_settings:VoiceXP=None, Level_roles_list=[], Non_level_roles_list=[]):
        self.server_name = None
        self.def_settings = def_settings #class obejct | Settings
        self.message_settings = message_settings #class object | XP settings
        self.voice_settings = voice_settings #class object | VoiceXP settings
        self.Level_roles_list = Level_roles_list
        self.Non_level_roles_list = Non_level_roles_list

    @staticmethod
    def preset_default() -> 'Server':
        "Creates a default Arcane (non-premium) server profile and returns it"
        #default main settings
        def_settings = Settings("linear" , 1 , float('inf') , True , False)

        #default message settings
        message_settings = XPSettings(15,40,60)

        #default voice settings
        voice_settings = VoiceXP(0,0,0,0) #voice xp is disabled for the default settings
        voice_settings.voice = False

        #Roles
        None
        
        default = Server(def_settings, message_settings, voice_settings,[],[])

        #returns a server object
        return default

    @staticmethod
    def preset_premium() -> 'Server':
        "Creates a default premium Arcane server profile and returns it"
        #default premium main settings
        def_settings = Settings("linear" , 1 , float('inf') , True , False)

        #default premium message settings
        message_settings = XPSettings(15,40,60)

        #default premium voice settings
        voice_settings = VoiceXP(15,40,180,2) 

        #Roles
        None
        
        premium = Server(def_settings, message_settings, voice_settings,[],[])

        #returns a server object
        return  premium

    @staticmethod
    def create_mdds() -> 'Server':       
        "Custom preset for the Murder Drones Discord Server profile and returns it"

        Role.empty_lists() #empty any existing roles in the lists
        #default main settings
        def_settings = Settings("linear" , 1 , float('inf') , False , False)

        #default message settings
        message_settings = XPSettings(15,40,60)

        #default voice settings
        voice_settings = VoiceXP(15,40,180,2) 

        #Roles
        baby_bean = LevelRole('baby_bean',0.1,0)
        worker_drone = LevelRole('worker_drone',0,5)
        murder_drone = LevelRole('murder_drone',0,35)
        cabin_fever_subject = LevelRole('cabin_fever_subject',0,60)
        level_role_list = [baby_bean,worker_drone,murder_drone,cabin_fever_subject]


        jcjenson_shareholder = NonLevelRole('jcjenson_shareholder',0.15)
        non_level_role_list = [jcjenson_shareholder]
        #role lists are stored within the role class
        
        mdds = Server(def_settings,message_settings,voice_settings,level_role_list,non_level_role_list)
        mdds.server_name = 'mdds'
        #returns a server object
        return mdds

    @staticmethod #for terminal UI only
    def create_custom() -> 'Server':
        "Creates a custom preset"

        print("WARNING: The custom server preset method is still WIP. Any data input will be erased when the program ends.")
        print("It requires much refining and polishing, , expect bugs.")

        server_name = input("\nWhat's your server's name?:")
        print("Let's start with the default XP settings:")
        curve = input("Curve (only 'Linear' supported currently):")
        multiplier = int(input("Multiplier (only value 1 supported currently):"))
        max_level = int(input("Max level (enter 0 if no limit):"))
        max_level = float('inf') if max_level == 0 else max_level
        stack_rewards = True if (input("Stack rewards y/n:") in ('y','yes','True')) else False
        stack_boosters = True if (input("Stack boosters y/n:") in ('y','yes','True')) else False

        def_settings = Settings(curve,multiplier,max_level,stack_rewards,stack_boosters)

        print("Onto the message XP settings:")
        min_xp = int(input("Minimum xp gained per message:"))
        max_xp = int(input("Maximum xp gained per message:"))
        cooldown = int(input("Cooldown between xp granting messages: "))

        message_xp = XPSettings(min_xp,max_xp,cooldown)

        check_if_voicexp = input("Do you have voice xp settings? y/n: ")
        if check_if_voicexp in ('y','yes','yeah'):
            voice_min_xp = int(input("Minimum voice xp gained per message:"))
            voice_max_xp = int(input("Maximum voice xp gained per message:"))
            voice_cooldown = int(input("Cooldown between xp being gained:"))
            
            voice_xp = VoiceXP(voice_min_xp,voice_max_xp,voice_cooldown,"can't even use that, who cares")
        else: 
            voice_xp = VoiceXP(0,0,0,0) #no settings basically
            voice_xp.voice = False

        check_if_lvl_roles = input("Are there level roles (xp boost or not)? y/n:")
        level_role_list = []
        if check_if_lvl_roles in ('y','yes','yeah'):
            counter = 0
            next_role = None
            
            print("Let's begin adding the level roles.\nFORMAT: <name>,<xpboost(float)>,<level>")
            print("Type 'end' to stop adding new roles")
            while(next_role != "end"):
                counter+=1
                next_role = input(f"Level Role {counter}:")
                if next_role == "end":
                    break
                name , boost, level = next_role.strip().split(",")
                level_role_list.append(LevelRole(name,float(boost),int(level)))

        check_if_nonlvl_roles = input("Are there non level roles that grant an xp boost? y/n:")
        non_level_role_list = []
        if check_if_nonlvl_roles in ('y','yes','yeah'):
            counter = 0
            next_role = None
            
            print("Let's begin adding the non level roles.\nFORMAT: <name>,<xpboost>")
            print("Type 'end' to stop adding new roles")
            while(next_role != "end"):
                counter+=1
                next_role = input(f"Non Level Role {counter}:")
                if next_role == "end":
                    break
                name , boost, level = next_role.strip().split(",")
                non_level_role_list.append(NonLevelRole(name,boost))
        
        custom = Server(def_settings,message_xp,voice_xp,level_role_list,non_level_role_list)
        custom.server_name = server_name
        
        return custom
        
    @staticmethod
    def my_own_custom():
        "TEMPLATE METHOD"
        "feel free to edit the content of this method to add your own server to the selection!"
        "You can follow the same format as the 'create_mdds()' method if you wish"

        #create your default main settings
        def_settings = Settings() #make sure to add the right attribute values

        #default message settings
        message_settings = XPSettings() #fill in your values

        #default voice settings
        voice_settings = VoiceXP() #fill in your values. Put 0 everywhere if your server doesn't have voice xp
        voice_settings.voice = True #set this to False if your server doesn't have voice xp enabled

        #Roles
        # lvlrole1 = LevelRole("rolename","xpboost(float)","level gained at")
        # levelrole2 = ...etc.
        level_role_list = [] #add all your lvl roles to that list

        # nonlvlrole1 = NonLevelRole("rolename","xpboost(float)")
        # nonlvelrole2 = ...etc.
        non_level_role_list = [] #add all your non-level roles in there
        # it is recommended to add only the roles which grant an xp boost for the non-level ones

        # Creating the server , no changes to this code required
        custom_server = Server(def_settings,message_settings,voice_settings,level_role_list,non_level_role_list)
        custom_server.server_name = "enter your server's name here"

        return custom_server


class UserConstants:
    #Store constants about the user that do not change
    def __init__(self,level_wanted=0, initial_level=0, initial_xp=0, chatperday=0, voiceperweek=0, voteboost=False
                  ):
        self.level_wanted = level_wanted
        self.initial_level = initial_level
        self.initial_xp = initial_xp
        self.chatperday = chatperday
        self.voiceperweek = voiceperweek
        self.voteboost = voteboost
        self.total_xp_needed = 0
        self.xp_segment_list = [] #list of xp needed per segment, where a segment is defined as the xp needed to reach the next level role
        self.roles_traversed = [] #list of level roles traversed to reach the target level

    def get_all_constants(self):
        return self.level_wanted,self.initial_level,self.initial_xp,self.chatperday,self.voiceperweek,self.voteboost
    
class UserDynamic:
    #store dynamic variables about the user that change as they level up
    def __init__(self):
        self.current_level = 0
        self.current_xp = 0
        self.user_roles = []
    
    def get_all_dynamic(self):
        return self.current_level,self.current_xp,self.user_roles
    
    def set_current_level(self,new_level):
        self.current_level = new_level

    def set_current_xp(self,new_xp):
        self.current_xp = new_xp

class User(UserConstants,UserDynamic):
    """User class, chatperday and voiceperweek are in minutes"""
    #Child class for the user, important for storing user-specific data
    def __init__(self,level_wanted=0,initial_level=0,initial_xp=0,chatperday=0,voiceperweek=0,voteboost=False #prompted values
                 ):
        
        UserConstants.__init__(self,level_wanted,initial_level,initial_xp,chatperday,voiceperweek,voteboost)
        UserDynamic.__init__(self)



    @staticmethod #for terminal UI only
    def create_user(server:Server) -> 'User' : #static method to create a user object by prompting the user for input
        "Prompts values to create a User object and returns it"
        try:
            level_wanted=int(input("Enter the level which you want to reach:"))
            initial_level=int(input("Enter the level you are at currently:"))
            initial_xp=int(input("Enter the amount of xp you currently have:"))
            chatperday=eval(input("How many minutes do you chat everyday?:"))
            if server.voice_settings.voice: #default doesn't have voice xp
                voiceperweek=eval(input('How many minutes do you speak in VC per week?:'))
            else:
                voiceperweek = 0
            voteboost=input("10% voteboost?y/n:-")

            voteboost=True if voteboost in ('y','yes','yeah') else False
        except TypeError:
            print("Invalid input, please try again")
            return User.create_user()

        user = User(level_wanted,initial_level,initial_xp,chatperday,voiceperweek,voteboost)
        user.current_level = initial_level
        user.current_xp = initial_xp
        
        return user
    
    @staticmethod #for terminal UI only
    def Selection_screen(failcount = 0):
        if failcount > 5:
            print("\nStopping the program. Failed attempt limit reached.")
            exit()


        print('''
The program you are running is designed to allow a user to get an estimate of the time they will need to spend
so as to reach a specific level in a Discord server. You will first be prompted with some possible presets.
        
Preset list:
1 : default (The default preset for arcane, that is: no role XP boosts, and no voice leveling)
2 : premium (Like default, but also includes voice leveling and message react leveling)
3 : mdds (This is the preset for the Murder Drones Discord Server)
4 : custom (Custom preset, more lengthy to set up but allows you to input custom Arcane Leveling settings, such as different random XP values)
    ''')
        
        selected_preset=input('Enter the selected preset:').lower()
        user : User
        if selected_preset in ('1','default'):
            server = Server.preset_default() #create server object
            user = User.create_user(server) #create user object
            preset_type = 'default'

        elif selected_preset in ('2','premium'): 
            server = Server.preset_premium() #create server object
            user = User.create_user(server) ; #create user object
            preset_type = 'premium'    

        elif selected_preset in ('3','mdds'):
            server = Server.create_mdds() #get server settings
            user = User.create_user(server) #create user
            user.prompt_non_level_roles(server) #prompt user for non-level roles
            
            preset_type = 'mdds'

        elif selected_preset in ('4','custom'):
            server = Server.create_custom()
            user = User.create_user(server)
            if len(server.Non_level_roles_list) > 0: user.prompt_non_level_roles(server)

            preset_type = 'custom' #for when it's functional
        
        elif selected_preset in ('0','exit','stop'):
            print("-"*40,"\nStopping the program.")
            exit()

        else:
            print("-"*40,"\nPlease enter a valid value or press 0 to exit the program.\n","-"*40)
            failcount+=1
            return User.Selection_screen(failcount)
        
        isValid, error_message = user.validation_checks(server)
        if not isValid:
            print(error_message) 
            failcount+=1
            return User.Selection_screen(failcount)

        user.target_xp(server) #obtain the total xp needed + xp per segment
        time_sum = user.message_xp_time(server) #obtain the time estimate in days
        user.display_time_estimate(time_sum,server) #display result
        return preset_type
    

    def validation_checks(self,server:Server):
        isValid = True
        error_reasons = "Following issues happened:"
        # level wanted < max level for server if any, be > 0, be > initial level. Integer
        # initial level >= 0, integer
        # initial xp >= 0, integer
        # 0 < chatperday <=1440
        # 0 <= voiceperweek <= 10,080

        if not((0 < self.level_wanted <= (server.def_settings.max_level)) and (self.level_wanted > self.initial_level)):
            error_reasons += "\nLevel wanted needs to:"
            if  not self.level_wanted < 0: error_reasons += " be a positive integer, "
            elif not self.level_wanted <= server.def_settings.max_level: error_reasons += " be less or equal to server's max level, "
            elif not self.level_wanted > self.initial_level: error_reasons += " be  greater than the initial level"
            isValid = False
        
        if not (self.initial_level >= 0):
            error_reasons += "\nInitial level needs to be a positive integer"
            isValid = False

        if not (self.initial_xp >= 0):
            error_reasons += "\nInitial xp needs to be a positive integer"
            isValid = False

        if not (0 < self.chatperday <= 1440):
            error_reasons += "\nTime spent chatting must be a positive integer and less than 1440 minutes"
            isValid = False

        if not (0 <= (self.voiceperweek if self.voiceperweek!=None else -1) <= 10080):
            if self.voiceperweek == None:
                pass
            else:
                error_reasons += "\nTime in VC weekly must be a positive integer and less than 10080 minutes"
                isValid = False
        if not isValid: error_reasons += "\nPlease try again\n" + "-"*60
        return (isValid,error_reasons)


    
    def prompt_non_level_roles(self, server : Server): #for terminal UI only

        non_level_list = server.Non_level_roles_list
        proper_selection = False
        while not proper_selection:
            print(f'{("-")*40}\nThe following roles provide an xp boost. Please select the one(s) you have.')
            role_number=0
            print('Enter 0 for none.')
            for role in non_level_list:
                role_number+=1 
                print(f'{role_number}:{role.get_name}')

            selected_role_num=input('Enter the number of the role(s) you have. Separate them with a comma.\nEnter 0 for none\n-:')
            if selected_role_num in ('0','none','no'):
                return self.user_roles #no update since no role added
            
            selected_role_num=selected_role_num.split(',')
            
            try:
                for role in selected_role_num:
                    role=int(role.strip())-1 #simply removing any whitespaces, -1 for the index offset
                    self.user_roles.append(non_level_list[role]) #using role num to append the actual rolename to the list
                    proper_selection=True
            except:
                print('Please input the choice in the valid format')
                continue
        return self.user_roles
    


    def add_role(self, role): #add any role to the user
        self.user_roles.append(role)

    def remove_all_level_roles(self, server : Server): #removes all level roles from the user
        for role in self.user_roles:
            if role in server.Level_roles_list:
                self.user_roles.remove(role)

    def update_level_roles(self, server : Server): #works using the current level
        
        settings = server.def_settings

        for role in server.Level_roles_list: #this loops adds any level roles the user has unlocked to our dynamic list
            
            if self.current_level >= role.get_level: #check if user can get this role
               
                if settings.stack_rewards==True: #stack lvl roles

                    self.user_roles.append(role) #simply add the role
               
                else: #don't stack lvl roles
                    
                    if server.Level_roles_list.index(role) == 0: #if index=0, then it means we are adding the first level roles. append.
                        self.remove_all_level_roles(server) #remove all level roles first
                        self.user_roles.append(role)
                        continue

                    else: #any following level role will be added and the previous one removed
                        #print([x.get_name for x in self.user_roles],role.get_name)
                        self.remove_all_level_roles(server)
                        self.user_roles.append(role)
                        #print([x.get_name() for x in user_roles],role.get_name())
                        
                        continue
            else:
                break #no more roles can be added
        #after this loop is completed, we now have the actual, updated list of roles the user has.
        return self.user_roles



    def target_xp(self, server : Server): #calculates the total and segment xp needed
        """Calculates and sets the user's total xp needed and xp needed for each level segment
        Returns a tuple (total XP needed,xp segment list). Those values are each attributes of user class"""
        
        '''
        general forumla for linear sum of xp till level n is:
        sum_till_n=50*(n**2)+125*n+75 where n>0 | scratch this formula, it's flawed
        better formula: S(n)= n/2 * [150 + (n - 1) * 100]
        where n is the level we want to reach
        '''
        #start by checking if level role stacks, if yes, use a stack algo

        sum_till_initial_xp = self.initial_level / 2 * (150 + (self.initial_level - 1) * 100) + self.initial_xp
        
        sum_till_wanted_xp = self.level_wanted / 2 * (150 + (self.level_wanted - 1) * 100)
        
        self.total_xp_needed = sum_till_wanted_xp - sum_till_initial_xp 
        

        #calculate sum of xp till next level role boundary

        previous_role_level = self.initial_level #not exactly previous role level but we need to initialise it
        previous_xp_sum = sum_till_initial_xp  #initialise the previous xp sum
        #keep track of which level roles were traversed


        for role in server.Level_roles_list:
            #print(role.get_level,self.initial_level,self.level_wanted)
            
            if role.get_level < self.initial_level: #skip any roles below the user's current level
                #print(f"{role.get_level} < {self.initial_level}")
                previous_role_level = role.get_level
                continue

            if self.initial_level > previous_role_level: #
                #print(f"{self.initial_level} > {previous_role_level}")
                if self.level_wanted < role.get_level: #if the person wants a level below the next role level, we can simply append the total xp needed and break
                    
                    
                    self.xp_segment_list.append(self.total_xp_needed)
                    break

                previous_role_level = self.initial_level
            

            if self.level_wanted < role.get_level:
                sum_till_next_level = self.level_wanted / 2 * (150 + (self.level_wanted - 1) * 100) - previous_role_level / 2 * (150 + (previous_role_level - 1) * 100)
                self.xp_segment_list.append(sum_till_next_level)
                #print(f"{self.level_wanted} < {role.get_level}")
                break

            sum_till_next_level = role.get_level / 2 * (150 + (role.get_level - 1) * 100) - previous_role_level / 2 * (150 + (previous_role_level - 1) * 100) #calculate the xp needed for the next role
            previous_role_level = role.get_level
           
            previous_xp_sum = sum_till_next_level
            self.roles_traversed.append(role)
            self.xp_segment_list.append(sum_till_next_level) #append the xp needed to the list

            if server.Level_roles_list[-1] == role and self.level_wanted > role.get_level: #if the loop is on the last role and the wanted level is above the level of the role
                
                sum_xp_above_last_role = self.level_wanted / 2 * (150 + (self.level_wanted - 1) * 100) - previous_role_level / 2 * (150 + (previous_role_level - 1) * 100)
                self.xp_segment_list.append(sum_xp_above_last_role)

        if self.xp_segment_list == []: #if the list is still empty
            self.xp_segment_list.append(self.total_xp_needed) #go with max xp needed

        #by now we have the total xp needed and the xp needed for each segment(from one specific level to another)  
        return self.total_xp_needed , self.xp_segment_list 

    def message_xp_time(self, server  : Server) -> int: #function to calculate msg xp
        """Calculates and returns the time taken to reach the desired level in xp/day units
        More complex method that takes into account roles and whether they or boosts stack.
        \nDEPENDS ON SEGMENT XP LIST"""

        if len(self.xp_segment_list) == 0: #catch in the event where segment list wasn't calculated yet
            self.target_xp(server)

        def_settings = server.def_settings
        xp_settings = server.message_settings
        voice_settings = server.voice_settings
        

        #start with the message xp settings
        mmin_xp = xp_settings.min_xp ; mmax_xp = xp_settings.max_xp ; mcooldown = xp_settings.cooldown
        vmin_xp = voice_settings.min_xp ; vmax_xp = voice_settings.max_xp ; vcooldown = voice_settings.cooldown 

        # Find the average boost (each boost per segment is averaged and then you multiply the total xp)
        #keep track of which roles the user has for each segment and apply relevant boosts.
        # add vote boost for as last

        maverage_xp = (mmax_xp + mmin_xp) / 2
        vaverage_xp = (vmax_xp + vmin_xp) / 2


        try:
            message_average_rate = maverage_xp / (mcooldown/60) #message xp per minute
        except ZeroDivisionError:
            message_average_rate = maverage_xp
        
        try:    
            voice_average_rate = vaverage_xp / (vcooldown/60) #voice xp per minute
        except ZeroDivisionError:
            voice_average_rate = vaverage_xp


        daily_message_rate = message_average_rate * self.chatperday #daily msg xp
        daily_voice_rate = voice_average_rate * (self.voiceperweek/7) #daily voice xp
        daily_xp_rate = daily_message_rate + daily_voice_rate

        xp_multiplier = 1.1 if self.voteboost == True else 1.0 #+10% multiplier if voteboost

        self.current_level = self.initial_level
        self.current_xp = self.initial_xp

        time_sum = 0

        #worth noting that stack reward is taken into account in the update_level_roles function
        #first condition is if boosts stack (excluding voteboost)
        if def_settings.stack_boosters:
            
            for segment in self.xp_segment_list:
                
                self.update_level_roles(server) #updates the user's roles based on current level for a segment
                #print([x.get_name for x in self.user_roles],[x.get_name for x in server.Level_roles_list]) ; print(server.Level_roles_list.index(self.user_roles[-1]) + 1,print(self.user_roles[-1].get_name),print())
                try:
                    self.current_level = server.Level_roles_list[server.Level_roles_list.index(self.user_roles[-1]) + 1].get_level #set the current level to the next level role
                except IndexError:
                    pass #index error means the user has the highest level role

                boosted_multiplier = xp_multiplier
                for role in self.user_roles: #add the boost from every role
                    boosted_multiplier += role.xpboost
                    
                
                boosted_daily_rate = daily_xp_rate * boosted_multiplier
                
                time_for_segment = segment / boosted_daily_rate #time in minutes for the segment
                
                #increment the time sum
                time_sum += time_for_segment
            
        else: #if boosts don't stack
            for segment in self.xp_segment_list:
                
                self.update_level_roles(server) #updates the user's roles based on current level for a segment
                #print([x.get_name for x in self.user_roles],[x.get_name for x in server.Level_roles_list]) ; print(server.Level_roles_list.index(self.user_roles[-1]) + 1,print(self.user_roles[-1].get_name),print())
                try:
                    self.current_level = server.Level_roles_list[server.Level_roles_list.index(self.user_roles[-1]) + 1].get_level #set the current level to the next level role
                except IndexError:
                    pass #index error means the user has the highest level role

                largest_boost = Role.find_largest_boost(self.user_roles) #find the largest boost from the user's roles
                
                boosted_multiplier = xp_multiplier + largest_boost
                
                boosted_daily_rate = daily_xp_rate * boosted_multiplier
                try:
                    time_for_segment = segment / boosted_daily_rate #time in minutes for the segment
                except ZeroDivisionError:
                    errorMessage = "You can't gain xp if you don't chat or speak in vc."
                    return print(errorMessage) if __name__ =='__main__' else errorMessage
                
                #increment the time sum
                time_sum += time_for_segment
                
        
        return time_sum #time in days

    def calculate_time_estimate(self,server : Server): #requires cleaning
        "This method returns the time estimates for message, voice and total (message + voice)"
        "Simple calcuation, that does not take into considerations roles"
        
        mmin_xp = server.message_settings.min_xp ; mmax_xp = server.message_settings.max_xp ; mcooldown = server.message_settings.cooldown #msg xp settings
        
        try: avg_m_xp = ((mmin_xp + mmax_xp)/2)/(mcooldown/60) #handling if cooldown = 0 or max xp = 0
        except ZeroDivisionError: return "fraudulent value, cooldown cannot be 0 and max_xp >0 and  > minxp"
        
        if self.voteboost: avg_m_xp *= 1.1

        minavg_chat_time = self.total_xp_needed / (avg_m_xp ) #minutes worth of xp, msg only
        
        if server.voice_settings.voice: #if voice xp settings present and enabled
            
            vmin_xp = server.voice_settings.min_xp ; vmax_xp = server.voice_settings.max_xp ; vcooldown = server.voice_settings.cooldown #voice xp settings
            
            try: avg_v_xp = ((vmin_xp + vmax_xp)/2)/(vcooldown/60) #handling if cooldown = 0 or max xp = 0    
            except ZeroDivisionError: return "fraudulent value, voice cooldown cannot be 0 and voice max_xp >0 and  > minxp" 
                
            if self.voteboost: avg_v_xp *= 1.1
            
            
            minavg_voice_time = self.total_xp_needed / (avg_v_xp ) #minutes worth of xp, voice only
            minavg_time = self.total_xp_needed / (avg_m_xp + avg_v_xp) #minutes worth of xp, msg and voice

        else: # in the event where no voice settings
            minavg_voice_time = 0 #no time estimate if no voice
            minavg_time = minavg_chat_time #set to the time estimate to that of the regular chatting one
            

        return minavg_chat_time , minavg_voice_time , minavg_time
    

    def get_time_estimate_variables(self,server = Server(),time_sum = False) -> tuple:
        "Works just like the display time estimate, but instead returns a list of variables"
        "that can be used by external programs if they wish to format the display with more control"
        if not time_sum: #in case time sum was not calculated yet
            time_sum = self.message_xp_time(server)
        
        minavg_chat_time , minavg_voice_time , minavg_time = self.calculate_time_estimate(server)
        
        time_display_variables = (
            minavg_chat_time, #rough time estimate
            minavg_voice_time, #rough time estimate
            minavg_time, #rough time estimate
            time_sum #role-based and daily chat time based estimate
        )
        #other variables should be accessed using the user attributes.

        return time_display_variables

    def display_time_estimate(self,time_sum,server = Server()) -> str: #display method for the time estimate
        "Method designed for display in the Terminal. Returns a string that can be used."
        #functional so far but needs refining, make it display differently if no voice xp

        minavg_chat_time , minavg_voice_time , minavg_time = self.calculate_time_estimate(server)
        
        #funny work around to print an error/string from a supposedly float variable
        if minavg_chat_time == str(minavg_chat_time): return print(minavg_chat_time)


        if server.voice_settings.voice: #if voice settings enabled

            display_text = f"""{"-"*45}
Here are the estimates:
            
Total XP needed to reach level {self.level_wanted}: {self.total_xp_needed}     
It would take {round(minavg_chat_time)} minutes if you only chat non-stop(no role boost)
It would take {round(minavg_voice_time)} minutes if you only voice chat non-stop(no role boost)
It would take {round(minavg_time)} minutes if you both chat and voice chat non-stop(no role boost)

Given you chat {self.chatperday} minutes daily and voice chat {self.voiceperweek} minutes weekly, taking into consideration boosts, roles and Arcane settings:

You would reach it in {round(time_sum)} day(s) or {round(time_sum*24,2)} hours or {round((time_sum*24*60),2)} minutes.
Note: The above estimate is more accurate given larger XP wanted to XP gained daily ratios.
It would take longer in reality given no human can send a message exactly when the cooldown ends.
{"-"*45}"""

        else:
            display_text = f"""{"-"*45}
Here are the estimates:
            
Total XP needed to reach level {self.level_wanted}: {self.total_xp_needed}     
It would take {round(minavg_chat_time)} minutes if you chat non-stop (no role boost)

Given you chat {self.chatperday} minutes daily, taking into consideration boosts, roles and Arcane settings:

You would reach it in {round(time_sum)} day(s) or {round(time_sum*24,2)} hours or {round((time_sum*24*60),2)} minutes.
Note: The above estimate is more accurate given larger XP wanted to XP gained daily ratios.
It would take longer in reality given no human can send a message exactly when the cooldown ends.
{"-"*45}"""            


        

        return print(display_text) if __name__ == '__main__' else display_text
    



def test_mdds():
    '''print('This is a test function to check if the code is running correctly.')
    Calculator.general_settings,Calculator.roles,Calculator.message_settings,Calculator.voice_settings=Preset.preset_mdds()
    Calculator.initialise_all_class_variables()
    Calculator.calculator_function()'''

    user = User(60,0,0,60,0,True) #create user
    print(user.get_all_constants())
    
    
    server = Server.create_mdds() #get server settings
    
    
    print(user.target_xp(server))
    #user.add_role(server.Non_level_roles_list[0]) #add the shareholder role
    
    print([x.get_level for x in user.roles_traversed])
    print("This is the time estimate:",user.message_xp_time(server),"days")

    """user.current_level = user.initial_level
    user.update_level_roles(server)
    print([x.get_name for x in user.user_roles],[x.get_name for x in server.Level_roles_list]) ; print(server.Level_roles_list.index(user.user_roles[-1]) + 1,print(user.user_roles[-1].get_name),print())
    try:
        user.current_level = server.Level_roles_list[server.Level_roles_list.index(user.user_roles[-1]) + 1].get_level #gonna need a try catch for index error here
    except IndexError:
        pass
    print(user.current_level)#; user.remove_all_level_roles(server)
    user.update_level_roles(server)
    print([x.get_name for x in user.user_roles]) ; print(server.Level_roles_list.index(user.user_roles[-1]) + 1,print(user.user_roles[-1].get_name))
    user.current_level = server.Level_roles_list[server.Level_roles_list.index(user.user_roles[-1]) + 1].get_level #gonna need a try catch for index error here
    print(user.current_level)
    user.update_level_roles(server)
    print([x.get_name for x in user.user_roles]) """
    
def test_default():
    user = User(60,0,0,60,0,True)
    server = Server.preset_default()

    print(user.target_xp(server))
    print(time_sum := user.message_xp_time(server))
    user.display_time_estimate(time_sum)

if __name__=='__main__':
    User.Selection_screen() #run the selection screen