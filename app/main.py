from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

#TODO Fix recitation hours to be correct for this semester.
RECITATION_HOURS = {"a": "09:00~09:50", "b": "10:00~10:50",
                    "c": "11:00~11:50", "d": "1:00~1:50",
                    "e": "2:00~2:50", "f": "3:00~3:50"}
MICROSERVICE_LINK = "http://17313-teachers2.s3d.cmu.edu:8080/section_info/"


@app.get("/section_info/{section_id}")
def get_section_info(section_id: str):

    if section_id is None:
        raise HTTPException(status_code=404, detail="Missing section id")

    section_id = section_id.lower()

    response = requests.get(MICROSERVICE_LINK + section_id)

    # You can check out what the response body looks like in terminal using the print statement
    data = response.json()
    print(data)
    ta_name_list = data["ta"]
    ta1_name = ta_name_list[0]
    ta2_name = ta_name_list[1]

    print(ta1_name)

    # TODO Fix this to return correct values for correct sections.
    if section_id in RECITATION_HOURS:
        return {
            "section": "Recitation " + section_id.upper(),
            "start_time": RECITATION_HOURS[section_id].split("~")[0],
            "end_time": RECITATION_HOURS[section_id].split("~")[1],
            "ta": [ta1_name, ta2_name]
        }
    else:
        raise HTTPException(status_code=404, detail="Invalid section id")
