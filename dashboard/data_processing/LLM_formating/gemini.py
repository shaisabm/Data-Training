# from google import genai
#
#
#
# registration = '93654500555_RegistrationReport(in).csv'
# participants = 'participants_93654500555(in).csv'
#
# prompt = """
#
# Registration
#
#    First Name   Last Name                        Email Registration Time Approval Status
# 0      Lyubov  Nakonechna            lnakonec@nyit.edu   1/10/2025 12:00        approved
# 1      Deanna       Edgar              dedgar@nyit.edu   1/10/2025 12:01        approved
# 2       Susan     Collins            scolli03@nyit.edu   1/10/2025 12:08        approved
# 3        Mick     Bradley        mick.bradley@nyit.edu   1/10/2025 12:10        approved
# 4      Eileen     Gazzola            egazzola@nyit.edu   1/10/2025 12:15        approved
# 5    Lorraine      Botros             lbotros@nyit.edu   1/10/2025 12:15        approved
# 6    Kimberly        Bowe               kbowe@nyit.edu   1/10/2025 12:17        approved
# 7        Jill      Rogers          jillrogers@nyit.edu   1/10/2025 12:35        approved
# 8       Sumin         Kim              skim70@nyit.edu   1/10/2025 12:42        approved
# 9     Mahnaz      Tehrani            mtehrani@nyit.edu   1/10/2025 13:24        approved
# 10    Jessica    Cernadas            jcernada@nyit.edu   1/10/2025 14:39        approved
# 11       Jian        Wang       missjianwang@gmail.com   1/11/2025 12:24        approved
# 12     Monika       Rohde        monika.rohde@nyit.edu   1/13/2025 10:05        approved
# 13     Martin      Gerdes             agerdes@nyit.edu   1/13/2025 13:55        approved
# 14     Vicky        Boyle              vboyle@nyit.edu   1/13/2025 14:33        approved
# 15   Nayoung          Kim              nkim04@nyit.edu   1/13/2025 16:03        approved
# 16    Natalie      Parkes             nparkes@nyit.edu    1/14/2025 9:41        approved
# 17    Lillian        Liao               lliao@nyit.edu   1/14/2025 13:50        approved
# 18  BettyAnn        Rizzo              brizzo@nyit.edu   1/15/2025 10:30        approved
# 19       Paul   Kutasovic            Pkutasov@nyit.edu   1/17/2025 20:19        approved
# 20    Tiffani       Hinds              tblake@nyit.edu   1/21/2025 10:52        approved
# 21  AnneMarie   Morrissey            amorriss@nyit.edu   1/21/2025 10:53        approved
# 22    Michael  Schiavetta  michael.schiavetta@nyit.edu   1/21/2025 14:45        approved
#
# participants:
#                                        Topic                     ID                                Host Duration (minutes)       Start time         End time  Participants
# 0   Byte-Sized Training: Zoom's AI Companion            93654500555  Jennifer Lawlor (jlawlor@nyit.edu)                 27  1/28/2025 13:30  1/28/2025 13:57           9.0
# 1                                        NaN                    NaN                                 NaN                NaN              NaN              NaN           NaN
# 2                       Name (original name)                  Email            Total duration (minutes)              Guest              NaN              NaN           NaN
# 3                            Jennifer Lawlor       jlawlor@nyit.edu                                  27                 No              NaN              NaN           NaN
# 4                              Susan Collins      scolli03@nyit.edu                                  27                Yes              NaN              NaN           NaN
# 5                              Kimberly Bowe         kbowe@nyit.edu                                  27                 No              NaN              NaN           NaN
# 6                                Jill Rogers    jillrogers@nyit.edu                                  26                 No              NaN              NaN           NaN
# 7                               Monika Rohde  monika.rohde@nyit.edu                                  26                 No              NaN              NaN           NaN
# 8                             Eileen Gazzola      egazzola@nyit.edu                                  26                 No              NaN              NaN           NaN
# 9                             Mahnaz Tehrani      mtehrani@nyit.edu                                  25                Yes              NaN              NaN           NaN
# 10                       AnneMarie Morrissey      amorriss@nyit.edu                                  24                Yes              NaN              NaN           NaN
# 11                              Lillian Liao         lliao@nyit.edu                                  27                 No              NaN              NaN           NaN
#
#
# You are a data formatting assistant. Your task is to convert input data into a specific JSON format.
#                      Follow these strict formatting rules:
#                      1. Output must be valid JSON
#                      2. Remove all newlines from the output
#                      3. Participants should be an array of objects containing ALL registrants
#                      4. Follow this exact structure:
#                      {
#                          "event": {
#                              "topic": string,
#                              "id": integer,
#                              "event_month": word form,
#                              "event_date": "m/d/yyyy",
#                              "event_time": string
#                          },
#                          "participants": [{
#                              "first_name": string,
#                              "last_name": string,
#                              "email": string,
#                              "duration": integer,
#                              "join_time": string,
#                              "leave_time": string,
#                              "attended": Yes/No
#                          },
#                          {
#                          ... additional participants ...
#                         }]
#                      }
#             Important Rules:
#             1. Participant Processing:
#                - Include ALL people from the registration list in the participants array
#                - Match participants data using email addresses
#                - For registrants who didn't attend (not in participants list):
#                   * Set duration to 0
#                   * Set join_time and leave_time to null
#                   * Set attended to false
#                - No duplicate participants (use email as unique identifier)
#                - If multiple entries exist for same email in participants list, add the durations
#
#             2. Time Format Requirements:
#                - event_time format: "HH:MM:SS AM/PM" (e.g., "01:00:00 AM")
#                - join_time format: "M/D/YYYY HH:MM:SS AM/PM" (e.g., "8/14/2024 1:30:42 PM")
#                - leave_time format: "M/D/YYYY HH:MM:SS AM/PM" (e.g., "8/14/2024 1:30:42 PM")
#                - All times must include seconds
#                - Use 12-hour format with AM/PM
#
#             3. Attendance Rules:
#                - 'attended' is Yes ONLY if:
#                   * Person appears in the participants list AND
#                   * Has duration >= 5 minutes
#                - 'attended' is No otherwise
#
#             4. Time Handling:
#                - If join_time is missing but person attended, use event start time with event date
#                - If leave_time is missing but person attended, use event end time with event date
#                - For non-attendees, use null for both join_time and leave_time
#
#             5. Data Consistency:
#                - Maintain consistent formatting for all participant entries
#                - Duration should be in minutes (integer)
#                - Email addresses should be lowercase
#                - Always include leading zeros in hours (e.g., "09:00:00 AM" not "9:00:00 AM")
#                - Always include seconds even if they're "00\""""
#
# client = genai.Client(api_key="AIzaSyA-F3BkUoG6oYCUQkoE8wPCBYnFMVW0VoE")
# response = client.models.generate_content(
#     model='gemini-2.0-flash',
#     contents=prompt,
# )
#
# # Use the response as a JSON string.
# print(response.text)