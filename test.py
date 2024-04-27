from llm_interfaces import Context, Form_groq, Agents

text= """Fusion Power: The Quest for a Clean Energy Future
What is Fusion Power?
Fusion power represents the pinnacle of clean energy, a process that mimics the reactions at the heart of stars. When two light atomic nuclei merge, they form a heavier nucleus and release a tremendous amount of energy. This process is the opposite of nuclear fission, which powers current nuclear reactors by splitting heavy atoms into lighter ones.

The Promise of Fusion
The allure of fusion power lies in its potential to provide a nearly limitless source of energy without the long-lived radioactive waste associated with fission reactors. Fusion fuel, derived from water and lithium, is abundant enough to satisfy global energy demands for millions of years. Moreover, fusion does not contribute to climate change, making it an environmentally friendly alternative to fossil fuels.

The Challenge of Containment
To achieve fusion, conditions similar to the sun’s core—temperatures of approximately 100 million kelvins—are required. At such extreme temperatures, matter exists in a plasma state. Containing this hot plasma long enough for fusion to occur is one of the greatest challenges. The Lawson criterion defines the necessary conditions for a net energy gain from fusion, which includes temperature, pressure, and confinement time.

Current Research and Breakthroughs
As of 2024, no fusion reactor has achieved net power output, but significant progress has been made. The most prominent fusion experiments today are the tokamak and inertial confinement fusion (ICF) by laser. The ITER tokamak in France and the National Ignition Facility (NIF) laser in the United States are leading the charge towards a viable fusion reactor1.

The Future of Fusion
The road to commercial fusion power is paved with both technical and economic challenges. However, the potential benefits to humanity are immense. As research continues to overcome the hurdles, the dream of a fusion-powered society moves closer to reality. With continued international collaboration and innovation, fusion power could revolutionize our energy systems and pave the way for a sustainable future.

This article provides a snapshot of the current state and potential of fusion power. For more detailed information, you can explore resources like the ITER project’s website2 or the latest scientific articles on the subject1. Fusion power is not just a scientific endeavor; it’s a vision of a cleaner, brighter future for all."""

response = Agents().extractor(text)

for information in response:
    print(Agents().question_asker(information))




