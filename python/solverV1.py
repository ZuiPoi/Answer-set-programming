
import os
import codecs
import sys
import clingo
from clyngor import ASP, solve
import string
import re
"""
Author Joshua Desmond
"""

def read_line(line):
    res = ()
    type =0
    list_params = line.strip().split(",")

    if (len(list_params) > 0):
        if(list_params[0] == "Module"):
            type = 1
            list_params[3] = int(list_params[3])
            list_params[4] = int(list_params[4])
            list_params[5] = int(list_params[5])
            list_params[6] = int(list_params[6])
            list_params.pop(0)
        if (list_params[0] == "Room"):
            type = 2
            list_params[2] = int(list_params[2])
            list_params[3] = int(list_params[3])
            list_params.pop(0)
        if (list_params[0] == "Curricula"):
            type = 3
            list_params.pop(0)
        if (list_params[0] == "UnavailConst"):
            type = 4
            list_params[2] = int(list_params[2])
            list_params[3] = int(list_params[3])
            list_params.pop(0)

        res = tuple(list_params)
    else:
        res = tuple(list_params)

    return type, res

def modif_outline(file, outfile):
      file = open(file, "r")
      outputfile  = open(outfile, "w")
      writeout = ""
      for line in file:
          list_params = line.strip().split(",")
          list_params.pop(0)
          
          nameOfModule = ""
          for char in list_params[0]:
              if char.isalpha():
                  nameOfModule += char
                  
          dayOfModule =   0
          for char in list_params[1]:
              if char.isdigit():
                  dayOfModule = char
                  
          timeOfModule =  0
          for char in list_params[2]:
              if char.isdigit():
                  timeOfModule = char 
                
          writeout = str(nameOfModule) + str(",") + str(dayOfModule) + str(",") + str(timeOfModule) + "\n"
          outputfile.write(writeout)
          
      file.close()
      outputfile.close()
      
def main(input_folder, output_file):
    #overall attributes
    overallAttributes = []
    Name = ""
    moduleCount = 0
    days= 0
    roomCount=0
    periodsPerDay = 0
    curriculaCount = 0
    constraintCOunt = 0
    minDailyLecture = 2
    maxDailyLecture = 5
    #attributes that are lists
    modules = []
    curricula = []
    rooms = []
    writeout = []
    unavailconstraints=[]

    directory = os.listdir(input_folder)

    for file in directory:
        with open(input_folder + file, "r") as infile:
            for line in infile:
                type, retline = read_line(line)
                #if type is 0 then we are talking about an overall attribute
                if (type == 0):
                    if retline[0]== "Name":
                        Name = retline[1]
                    if retline[0]== "Modules":
                        moduleCount = retline[1]
                    if retline[0]== "Rooms":
                        roomCount = retline[1]
                    if retline[0]== "Days":
                        days = retline[1]
                    if retline[0]== "PeriodsPerDay":
                        periodsPerDay = retline[1]
                    if retline[0]== "Curriculan":
                        curriculaCount = retline[1]
                    if retline[0]== "Constraints":
                        constraintCOunt = retline[1]

                if(type==1):
                    modules.append(retline)
                if(type==2):
                    rooms.append(retline)
                if(type==3):
                    curricula.append(retline)
                if(type==4):
                    unavailconstraints.append(retline)

            infile.close()

    #hard constraints
    writeout.append("c(C) :- course(C,_,_,_,_,_). t(T) :- course(_,T,_,_,_,_).\n")
    writeout.append("r(R) :- room(R,_,_). cu(Cu) :- curricula(Cu,_).\n")
    writeout.append("d(0..D-1) :- days(D). ppd(0..P-1) :- periods_per_day(P).\n \n")
    writeout.append("N { assigned(C,D,P) : d(D), ppd(P) } N :- course(C,_,N,_,_,_).\n \n")
    writeout.append(":- not { assigned(C,D,P) : course(C,T,_,_,_,_) } 1, t(T), d(D), ppd(P).\n")
    writeout.append(":- not { assigned(C,D,P) : curricula(Cu,C) } 1, cu(Cu), d(D), ppd(P).\n \n")
    writeout.append("{ assigned(C,R,D,P) : r(R) } 1 :- assigned(C,D,P).\n")
    writeout.append(":- not { assigned(C,R,D,P) : c(C) } 1, r(R), d(D), ppd(P).\n \n")
    writeout.append(":- assigned(C,D,P), unavailability_constraint(C,D,P).\n")
    writeout.append(":- not { assigned(C,D,P) : c(C) } N, d(D), ppd(P), rooms(N).\n \n \n")


    #soft constraints
    writeout.append("penalty(\"RoomCapacity\",assigned(C,R,D,P),(N-Cap)*weight_of_s1) :- assigned(C,R,D,P), course(C,_,_,_,N,_), room(R,Cap,_), N > Cap.\n \n")
    writeout.append("penalty(\"StudentMinMaxLoad\",student_min_max_load(Cu,D,N,many),(N-Max)*weight_of_s6) :- cu(Cu), d(D), N = { scheduled_curricula(Cu,D,P) }, min_max_daily_lectures(Min,Max), N > Max. \n \n")
    #writeout.append("\n")
    #writeout.append("\n")
    
    
    
    
    
    k = len(modules)
    i = 0
    writeout.append("name(\""+Name+"\"). courses("+str(moduleCount)+"). rooms("+str(roomCount)+"). days("+str(days)+").periods_per_day("+str(periodsPerDay)+"). curricula("+str(curriculaCount)+").\n"
    +"min_max_daily_lectures("+str(minDailyLecture)+","+str(maxDailyLecture)+"). unavailabilityconstraints("+str(constraintCOunt)+"). roomconstraints("+"0"+").")
    writeout.append("\n \n")
    while i < k:
        if i== k/2:
            writeout.append("\n")

        m = modules[i]
        t = "course(\""+ str(m[0]) +"\",\""+ str(m[1])+"\"," +str(m[2])+"," +str(m[3])+","+str(m[4])+","+str(m[5])+")"
        writeout.append(t)
        writeout.append(". ")
        i=i+1

    writeout.append("\n \n")

    i = 0
    k = len(rooms)

    while i < k:
        if i== k/2:
            writeout.append("\n")

        m = rooms[i]
        t = "room(\""+ str(m[0]) +"\","+ str(m[1])+str(m[2])+")"
        writeout.append(t)
        writeout.append(". ")
        i=i+1
    writeout.append("\n \n")

    i = 0
    k = len(curricula)

    while i < k:
        if i== k/2:
            writeout.append("\n")
        l = curricula.copy()
        m = list(l[i])
        curricName = m[0]
        m.pop(0)
        lencur = len(m)
        p = 0
        while p<lencur:
            t = "curricula(\""+ str(curricName) +"\",\""+ str(m[p])+"\")"
            writeout.append(t)
            writeout.append(". ")
            p=p+1

        i=i+1
    writeout.append("\n \n")

    i = 0
    k = len(unavailconstraints)

    while i < k:
        if i== k/2:
            writeout.append("\n")

        m = unavailconstraints[i]
        t = "unavailability_constraint(\""+ str(m[0]) +"\","+ str(m[1])+","+ str(m[2])+")"
        writeout.append(t)
        writeout.append(". ")
        i=i+1
    writeout.append("\n \n")
    writeout.append("#show assigned/3.")
    writeout.append("\n \n")
    writeout.append('#defined addTab/2.')
    k = len(writeout)
    i = 0

    with open(output_file, "w") as outfile:
        while i < k:
            outfile.write(writeout[i])
            i = i + 1
        outfile.close()


if __name__ == "__main__":
    input_folder = "../datasets/"
    output_file = "../results/result.lp"
    result_output_file = "../results/result.txt"
    final_output_file = "../Webserver/static/result_for_web.txt"
    main(input_folder,output_file)
   # modif_outline(result_output_file, final_output_file)
    
    #take the first answer set created and write it out, then format it for use with the webeserver
    outputfile  = open(result_output_file, "w")
    answers = solve(output_file)
    x=0
    for answer in answers:
        x=x+1
        print("Set")
        for i in answer :
            print(str(i))
            outputfile.write(str(i)+ "\n")
        if x == 1:
            outputfile.close()
            modif_outline(result_output_file, final_output_file)
            break

