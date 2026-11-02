# Divineesates — Property Film Studio

**Divineesates** is a Python-powered property video creation platform that transforms verified property details and 4–8 photographs into professional, shareable MP4 property films.

Designed with a premium luxury aesthetic, Divineesates features a warm brown and burgundy color palette, elegant interface, horizontal navigation, and a simple four-step workflow.

The platform helps real estate professionals, property owners, and agents create engaging property showcase videos without requiring professional video-editing skills.

## Features

- **Property Details Management:** Add property name, location, type, price, area, rooms, description, and verified features.
- **Photo Management:** Upload, remove, reorder, and customize property photographs.
- **Scene Customization:** Edit captions and select visual styles for individual scenes.
- **AI-Assisted Script Generation:** Generate structured property narration using template-based logic.
- **Multiple Video Formats:** Export videos in 16:9, 9:16, and 1:1 aspect ratios.
- **Narration Support:** Optional English text-to-speech narration.
- **Background Music:** Add optional user-provided audio.
- **MP4 Export:** Generate, preview, and download completed property videos.
- **Luxury UI:** Responsive interface with a premium brown and burgundy theme.

## Installation and Setup (Windows)

### 1. Extract the Project

Extract the downloaded ZIP file.

### 2. Open Command Prompt

Open CMD inside the `EstateFrame_Studio` project folder (the folder containing `requirements.txt` and `estateframe_server.py`).

### 3. Create a Virtual Environment

```cmd
py -3.14 -m venv .venv
```

### 4. Activate the Virtual Environment

```cmd
.venv\Scripts\activate
```

### 5. Upgrade pip

```cmd
python -m pip install --upgrade pip
```

### 6. Install Dependencies

```cmd
pip install -r requirements.txt
```

### 7. Start Divineesates

```cmd
python estateframe_server.py
```

After successful startup, the terminal should display:

```text
Divineesates Studio running at http://localhost:8000
```

### 8. Open the Application

Open your browser and visit:

**http://localhost:8000**

Keep the Command Prompt window running while using the application.

To stop the server, press `Ctrl + C` in Command Prompt.

### Troubleshooting

If the virtual environment is broken, remove it:

```cmd
rmdir /s /q .venv
```

Recreate it:

```cmd
py -3.14 -m venv .venv
```

Activate it:

```cmd
.venv\Scripts\activate
```

If `pip` is not recognized, use:

```cmd
python -m pip install -r requirements.txt
```

## How Divineesates Works

The application follows a simple four-step property video creation workflow.

### Step 1: Enter Property Details

Provide the property name, location, property type, price, optional room and area information, description, verified features, enquiry text, and optional branding.

### Step 2: Upload Property Photographs

Upload 4–8 property photographs in JPG, JPEG, or PNG format.

- Maximum image size: 10 MB per image.
- Remove unwanted photographs.
- Reorder images.
- Customize individual scene captions.

### Step 3: Customize the Property Film

- Select a visual style.
- Choose the output format: 16:9, 9:16, or 1:1.
- Review and edit the generated narration script.
- Enable optional text-to-speech narration.
- Add optional background music.

### Step 4: Generate and Download

Generate the final MP4 property film, preview it directly inside the application, and download the exported video.

## Project Structure

```text
Divineesates_Studio/
│
├── .streamlit/
├── assets/
├── outputs/
├── sample_output/
├── tests/
├── web/
│
├── app.py
├── components.py
├── styles.py
├── script_engine.py
├── video_engine.py
├── estateframe_server.py
│
├── sample_property.json
├── requirements.txt
├── README.md
├── run_app.bat
└── run_3d.bat
```

### Core Components

| File | Description |
|---|---|
| `app.py` | Application interface, page routing, state management, validation, and MP4 export |
| `styles.py` | Responsive UI styling and luxury theme |
| `components.py` | Cover preview and workflow stepper |
| `script_engine.py` | Template-based narration and scene planning |
| `video_engine.py` | Video animation, overlays, transitions, audio, and MP4 encoding |
| `estateframe_server.py` | Application server |
| `sample_property.json` | Fictional sample property information |
| `requirements.txt` | Python dependencies |

## Technologies Used

- **Python:** Core application logic.
- **Streamlit:** Interactive application framework.
- **Pillow:** Image processing and scene creation.
- **NumPy:** Image and frame manipulation.
- **imageio-ffmpeg:** MP4 video encoding.
- **gTTS:** Optional English text-to-speech narration.
- **Matplotlib:** Visualization support.
- **SQLite:** Data persistence.
- **HTML and CSS:** Web interface customization.

## Models, Libraries, and Limitations

**Script Generation:** Uses deterministic, template-based logic. No external LLM API is currently configured. All generated text is based on property details and captions supplied by the user.

**Narration:** Optional English text-to-speech using gTTS. Internet access is required. If narration fails, video export can continue without it.

**Video Rendering:** Pillow and NumPy generate animated image scenes and text overlays. imageio-ffmpeg handles H.264 MP4 encoding. Crossfade transitions are included between scenes.

**Background Music:** Supports optional user-provided audio files. Only use music that you have permission to publish.

**History:** Session-based history does not persist after the Streamlit session ends.

**Sample Data:** Demo photographs and property listings are generated synthetic examples. Replace them with authorized property photographs and verified property details before publishing.

## Video Output Specifications

The renderer validates that each property video contains 4–8 valid images and handles missing optional information by excluding it from the generated copy.

| Format | Resolution | Use Case |
|---|---|---|
| Landscape (16:9) | 1280 × 720 | YouTube and property presentations |
| Portrait (9:16) | 720 × 1280 | Instagram Reels and YouTube Shorts |
| Square (1:1) | 1080 × 1080 | Social media posts |

Generated videos are saved in the `outputs/` directory.

The bundled sample MP4 uses a smaller resolution to keep the project download size compact.

## Project Vision

**Divineesates — Turning Property Details into Premium Property Films.**

Our goal is to simplify real estate marketing by making professional-looking property videos accessible, customizable, and easy to create.

Divineesates combines property information, visual storytelling, and automated video rendering into one streamlined platform.
