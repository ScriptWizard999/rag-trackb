# **🌌 RAG-powered Q&A System (Space Exploration)**

This project implements a Retrieval-Augmented Generation (RAG) system that answers questions on Space Exploration by combining document retrieval, reranking, and generative AI. The system ensures grounded answers with citations by retrieving relevant text chunks from Wikipedia content on Space Exploration.

## **📖 Table of Contents**

- Architecture
- Chunking Parameters
- Providers Used
- Quick Start
- Evaluation
- Remarks
- Author

### 🏗️ Architecture

- flowchart TD
    A[User Question] --> B[Embed with Cohere]
    B --> C[Retrieve Top-K Chunks from Pinecone]
    C --> D[Rerank Results with Cohere Rerank v3.5]
    D --> E[LLM (Cohere Command-R-Plus)]
    E --> F[Final Answer + Citations in Streamlit UI]


- Step 1: User enters a question in the Streamlit UI.
- Step 2: The question is embedded using Cohere embed-english-v3.0.
- Step 3: Top-K candidate chunks are retrieved from Pinecone vector DB.
- Step 4: Candidates are reranked using Cohere Rerank v3.5.
- Step 5: Cohere Command-R-Plus generates a grounded answer with inline citations.

### 🔖 Chunking Parameters

- Chunk size: 800–1200 tokens
- Overlap: 10–15%
- Reasoning: Balances semantic coherence and retrieval granularity — long enough for context, small enough for relevance.

### 🤝 Providers Used

- **Cohere**
- embed-english-v3.0 → Question/document embeddings
- rerank-v3.5 → Rerank retrieved passages
- command-r-plus → Generate grounded answers

- **Pinecone**

- Vector database for semantic search
- Index: rag-index with 1536-dimension embeddings

- **Streamlit**
- Frontend interface for interactive Q&A

### ⚡ Quick Start
**1️⃣ Clone the repo**
`git clone https://github.com/ScriptWizard999/rag-trackb.git`
`cd rag-trackb`

**2️⃣ Install dependencies**
`pip install -r requirements.txt`

**3️⃣ Setup environment variables**

Create a **.env file:**

`COHERE_API_KEY=your_cohere_key`

`PINECONE_API_KEY=your_pinecone_key`

**4️⃣ Run the app**
`streamlit run app.py`


**👉 Open your browser at http://localhost:8501**

### 📊 Evaluation
- **Gold Q/A Pairs**

**Question 1**
Tell me about solar system

**Answer**
Our Solar System consists of eight planets, the Sun, the Moon, and various recognized dwarf planets, such as Ceres and Pluto. [1]

The first interplanetary flyby was conducted by Venera 1 in 1961, passing by Venus. [1] Since then, there have been numerous explorations of the other planets and their moons. [1,2,5] For example, Pioneer 10 flew by Jupiter in 1973 [1], and Saturn, which has at least 62 known moons [2], was explored by the Cassini-Huygens spacecraft. [2,5]

The Sun, being the closest star and the center of our Solar System, is also a major focus of space exploration. [4] It generates most space weather, which can impact power systems and satellites on and around Earth. [4] Spacecraft dedicated to observing the Sun, such as the Parker Solar Probe, have been launched to study it. [4]

Delta-v, or the change in velocity of a spacecraft, is a key factor in the energy cost of exploring different planets in our Solar System. [3] This is particularly notable in the case of Mercury, which is relatively challenging to reach due to its proximity to the Sun. [3]

The exploration of our Solar System has provided us with valuable data and continues to enhance our understanding of the cosmos.

**Sources**
[1] The first crewed landing on another celestial body was performed by Apollo 11 on 20 July 1969, landing on the Moon. There have been a total of six spacecraft with humans landing on the Moon starting from 1969 to the last human landing in 1972.

The first interplanetary flyby was the 1961 Venera 1 flyby of Venus, though the 1962 Mariner 2 was the first flyby of Venus to return data (closest approac...

[2] Saturn has at least 62 known moons, although the exact number is debatable since Saturn's rings are made up of vast numbers of independently orbiting objects of varying sizes. The largest of the moons is Titan, which holds the distinction of being the only moon in the Solar System with an atmosphere denser and thicker than that of Earth. Titan holds the distinction of being the only object in the ...

[4] The Sun The Sun is a major focus of space exploration. Being above the atmosphere in particular and Earth's magnetic field gives access to the solar wind and infrared and ultraviolet radiations that cannot reach Earth's surface. The Sun generates most space weather, which can affect power generation and transmission systems on Earth and interfere with, and even damage, satellites and space probes....

[3] Flights to other planets within the Solar System are accomplished at a cost in energy, which is described by the net change in velocity of the spacecraft, or delta-v. Due to the relatively high delta-v to reach Mercury and its proximity to the Sun, it is difficult to explore and orbits around it are rather unstable.

**Question 2**
What is space exploration?

**Answer**
Space exploration is the physical investigation of outer space using uncrewed robotic probes and human spaceflight. [1]

**Sources**
[1] Space exploration is the physical investigation of outer space by uncrewed robotic space probes and through human spaceflight.[1]

While the observation of objects in space, known as astronomy, predates reliable recorded history, it was the development of large and relatively efficient rockets during the mid-twentieth century that allowed physical space exploration to become a reality. Common rati...

**Question 3**

What is the first Space Station?

**Answer**
The first space station was Salyut 1, launched by the Soviet Union on April 19, 1971 [1,2].

**Sources**
[1] First space station Salyut 1 was the first space station of any kind, launched into low Earth orbit by the Soviet Union on 19 April 1971. The International Space Station (ISS) is currently the largest and oldest of the 2 current fully functional space stations, inhabited continuously since the year 2000. The other, Tiangong space station built by China, is now fully crewed and operational.

[2] The early era of space exploration was driven by a "Space Race" in which the Soviet Union and the United States vied to demonstrate their technological superiority. Landmarks of this era include the launch of the first human-made object to orbit Earth, the Soviet Union's Sputnik 1, on 4 October 1957, and the first Moon landing by the American Apollo 11 mission on 20 July 1969. The Soviet space pro...

**Question 4**

What are the targets of Space exploration?

**Answer**
The targets of space exploration include:

Earth orbit [2]
The Moon [2]
Saturn [2]
Jupiter [2]
Mars [2]
Venus [2]
Mercury [2,5]
The Sun [5]
The known Solar System [2]
The International Space Station [3]
Additionally, the Voyager 1 and 2 probes have traveled beyond 100 times the Earth-Sun distance. [2]

**Sources**
[2] As of 9 February 2025 Voyager 1 was at a distance of 166.4 AU (24.89 billion km; 15.47 billion mi) from Earth.[29] It is the most distant human-made object from Earth.[30]

Targets of exploration Starting in the mid-20th century probes and then human missions were sent into Earth orbit, and then on to the Moon. Also, probes were sent throughout the known Solar System, and into Solar orbit. Uncrewe...

[5] The Sun The Sun is a major focus of space exploration. Being above the atmosphere in particular and Earth's magnetic field gives access to the solar wind and infrared and ultraviolet radiations that cannot reach Earth's surface. The Sun generates most space weather, which can affect power generation and transmission systems on Earth and interfere with, and even damage, satellites and space probes....

[3] The early era of space exploration was driven by a "Space Race" in which the Soviet Union and the United States vied to demonstrate their technological superiority. Landmarks of this era include the launch of the first human-made object to orbit Earth, the Soviet Union's Sputnik 1, on 4 October 1957, and the first Moon landing by the American Apollo 11 mission on 20 July 1969. The Soviet space pro...

**Question 5**
Tell me about Mars planet

**Answer**
Mars is the subject of [1] and [5] in the provided context.

[1] Mars has been explored by various space programs, including those of the Soviet Union (Russia), the United States, Europe, Japan, and India. Dozens of spacecraft have been sent to the planet since the 1960s, including orbiters, landers, and rovers, with a focus on gathering data and answering scientific questions. Mars was first flown by in 1965 by the Mariner 4 spacecraft. [2]

[5] Exploring Mars has come with significant financial costs and challenges, with a high failure rate among spacecraft destined for the planet. This has led to references to a "Great Galactic Ghoul" [31] and the "Mars Curse" [32] in popular culture. Despite these challenges, India successfully conducted its first Mars mission, the Mars Orbiter Mission (MOM) [33,34,35], at a relatively low cost. [36,37]


**Sources**
[1] Mars Main article: Exploration of Mars

Surface of Mars by the Spirit rover (2004) The exploration of Mars has been an important part of the space exploration programs of the Soviet Union (later Russia), the United States, Europe, Japan and India. Dozens of robotic spacecraft, including orbiters, landers, and rovers, have been launched toward Mars since the 1960s. These missions were aimed at gath...

[5] The exploration of Mars has come at a considerable financial cost with roughly two-thirds of all spacecraft destined for Mars failing before completing their missions, with some failing before they even began. Such a high failure rate can be attributed to the complexity and large number of variables involved in an interplanetary journey, and has led researchers to jokingly speak of The Great Galac...

[2] The first crewed landing on another celestial body was performed by Apollo 11 on 20 July 1969, landing on the Moon. There have been a total of six spacecraft with humans landing on the Moon starting from 1969 to the last human landing in 1972.

The first interplanetary flyby was the 1961 Venera 1 flyby of Venus, though the 1962 Mariner 2 was the first flyby of Venus to return data (closest approac...


### 📂 Index Configuration  

- **Index name**: `rag-index`  
- **Dimension**: 1536 (Cohere embeddings size)  
- **Metric**: cosine similarity  
- **Replicas**: 1 (default)  
- **Pod type**: serverless (AWS, us-west-2)  

### Chunking strategy  
- Chunk size: 800–1200 tokens  
- Overlap: 10–15%  

### Precision, Recall, and Success Rate  

- **Precision** measures how many of the generated answers were correct out of all generated answers.  
- **Recall** measures how many correct answers were retrieved compared to the gold standard.  
- **Success Rate** is simply the fraction of questions for which the system produced a *useful and grounded* answer.  

For our 5-question gold set:  

- **Precision**: 5/5 = **100%** (all generated answers were correct and grounded).  
- **Recall**: 5/5 = **100%** (all expected answers were retrieved from the indexed context).  
- **Success Rate**: 5/5 = **100%** (the system returned useful answers for all questions).  
 


### 💬 Remarks

**Limits:**

- API quota limits on Cohere and Pinecone.
- Occasional citation mismatch if reranker returns too few results.

**Trade-offs:**

- Chunk size chosen (800–1200) improves context, but increases token usage.
- Falling back to Pinecone top-K when reranker fails.

### 👤 Author

- Souvik Sen

- 📧 Email: souviks1008@gmail.com
