import io
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
import pandas as pd
from api.modules.processing.utils.csv_process import generate_chart
from core import dependencies as deps
from . import schemas
from db.models.location import Location
import matplotlib.pyplot as plt


router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(
        file: UploadFile = File(...), 
        session = deps.get_session()
) -> schemas.UploadCSVResponse:
    """
    Upload a CSV file with columns: Область, Місто/Район, Значення
    and save data to the database.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
    
    content: bytes = await file.read()
    try:
        df: pd.DataFrame = pd.read_csv(io.StringIO(content.decode("utf-8-sig")))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV format: {e}")
    
    expected_columns: list[str] = ["Область", "Місто/Район", "Значення"]
    if not set(expected_columns).issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail=f"CSV must contain columns: {expected_columns}. Found: {list(df.columns)}"
        )

    records_to_insert = []
    for _, row in df.iterrows():
        try:
            value = float(row["Значення"])
        except ValueError:
            continue
        location = Location(
            region=row["Область"],
            district=row["Місто/Район"],
            value=value
        )
        records_to_insert.append(location)
        
    if records_to_insert:
        async with session.async_() as db:
            db.add_all(records_to_insert)
            await db.commit()

    return schemas.UploadCSVResponse(
        inserted_count=len(records_to_insert),
        message="CSV file processed successfully."
        )


@router.post("/generate-chart/")
async def create_chart(
    file: UploadFile = File(...),
    group_field: str = Form(default="Область"),
    value_field: str = Form(default="Значення"),
    title: str = Form(default="Середнє значення по областях"),
) -> StreamingResponse:
    df: pd.DataFrame = pd.read_csv(file.file, encoding="utf-8-sig")
    
    try:
        fig, _ = generate_chart(
            csv_file=df,
            group_field=group_field,
            value_field=value_field,
            title=title,
            save=False,
        )
    except ValueError as e:
        return {"error": str(e)}

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
