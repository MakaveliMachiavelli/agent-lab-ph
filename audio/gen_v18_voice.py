import asyncio
from edge_tts import Communicate
import os

async def main():
    voice = "fil-PH-BlessicaNeural"
    text = "Stop. Pagod ka na bang tuwing gabi, habang iniisip ang trabaho? Hindi ka nag-iisa. 81% ng Pinoy freelancers, gabi-gabi pa rin ang naghihintay sa trabaho. Pero... ano nga ba kung may robot na ang kumukuha ng trabaho para sa'yo? Habang ka ang natutuwa, kumukuha na ang robot ng pera. Tatlong simple step lang. Walang coding. Walang complex na set-up. Step 1: Bukas mo lang ang browser mo. OnlineJobs. Upwork. Libre. Step 2: I-click mo lang ang run. Hindi mo kailangang sumulat ng cover letter. Step 3: Hayaan mo kang matulog. Habang ikaw, natutulog ang robot. Robot na robot ang sumusubay-subay sa job listings. Kapag may perfect match, i-a-apply na agad. Narito ang proof. Python agent.py target equals onlinejobs. Found 2847 jobs matching customer support. Writing personalized cover letter 94 percent match. Applying to customer success rep at 8 dollars per hour. SUCCESS! Proposal submitted. Found data entry specialist at 6 dollars per hour. Applied. 52 jobs applied tonight. 52 applications. Isang gabi lang. Habang ikaw, natutulog. 15 interviews. 8 job offers. 3200 dollars per month. Hindi ito get rich quick scheme. Ito ay get rich while you sleep system. 15-min setup. One-time. Then 24-7 automatic. Legal? Oo. Ethical? Oo. Pinoy-tested? 100 plus freelancers na gumagamit. Gusto mo rin? Comment robot sa baba. I-sesend ko sa'yo ang libreng step-by-step guide. 15-min setup. Zero code. Walang hidden fees. Ang unang 500 lang. First come, first served. Hindi ito forever. After 500, closed na. Comment robot. Now. Bago matapos ang video. Agent Lab PH. Built by Dice. Para sa Pinoy freelancers."
    comm = Communicate(text, voice)
    await comm.save("./jobbot_v18_voice.mp3")
    print("Saved jobbot_v18_voice.mp3")

asyncio.run(main())
