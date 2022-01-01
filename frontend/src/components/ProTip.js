import * as React from 'react';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField'
import Grid from '@mui/material/Grid'
import Button from '@mui/material/Button';
import {inferHandler} from '../handlers/infer'

export default function ProTip() {

  const [difference, setDifference] = React.useState("0")
  const [gender, setGender] = React.useState("NB")
  const [height, setHeight] = React.useState("0")
  const [weight, setWeight] = React.useState("0")
  const [result, setResult] = React.useState("")

  const isFloatString = str => {
    return /^\d+\.\d+$|^\d+$/.test(str);
  }

  const isValidGender = val => {
    return (val.toUpperCase() == "M" || val.toUpperCase() == "F" || val.toUpperCase() == "NB")
  }

  const genderTranslate = s => {
    const str = s.toUpperCase()
    if (str == "M") {
      return 0
    }
    if (str == "F") {
      return 1
    }
    else {
      return 0.5
    }
  }

  const submitHandler = async () => {
    const inputValid = (isFloatString(difference) && isFloatString(height) && isFloatString(weight) && isValidGender(gender))
    if (!inputValid) {
      setResult("Ensure that your inputs are all numbers (except gender which should be one of M, F, or NB).")
    }
    else {
      const obj = {
        "difference": Number(difference),
        "gender": genderTranslate(gender),
        "height": Number(height),
        "weight": Number(weight)
      }
      setResult("Computing your highest grade prediction. Please allow up to ~15 seconds of processing time in the case of server cold start.")
      const ret = await inferHandler(obj)
      setResult(`V${ret.toString()}`)
    }
}

  const handleDifference = (event) => {
    if (!isFloatString(event.target.value)) {
    }
    setDifference(event.target.value)
  }

  const handleGender = (event) => {
    const val = event.target.value
    setGender(val)
  }

  const handleHeight = (event) => {
    setHeight(event.target.value)
  }

  const handleWeight = (event) => {
    setWeight(event.target.value)  
  }

  return (
    <Grid
      container
    >
      <Grid item xs={12}>
        <Typography sx={{ mt: 6, mb: 3 }} color="text.secondary">
          A random forest model that returns its best guess at your HIGHEST climbing V-grade given physical data. 
          <br></br> <br></br>
          Don't take the results too seriously. The data it was trained on is heavily biased with male, average-height, skinny climbers with 5-6 years of experience.
          On average, the model is off by about 2 V-levels. It was trained only on outdoor climbs. 
          
          <br></br> <br></br>
          This will certainly be inaccurate if you climb more than V8.
          <br></br> <br></br>

          <a href="https://www.kaggle.com/dcohen21/8anu-climbing-logbook">data</a> <br></br>
          <a href="https://github.com/rishabhsamb/rock-climbing-regressor">github</a>
        </Typography>
      </Grid>
      <Grid
        item
        xs={12}
        style={{ display: "flex", gap: "1rem", alignItems: "center", paddingBottom: 25 }}
      >
        <TextField 
          id="outlined-basic" 
          label="How long have you been climbing? (in years)" 
          variant="outlined" 
          fullWidth
          value={difference}
          onChange={handleDifference}
        />
      </Grid>
      <Grid
        item
        xs={12}
        style={{ display: "flex", gap: "1rem", alignItems: "center", paddingBottom: 25 }}
      >
        <TextField 
          id="outlined-basic" 
          label="Gender (M, F, NB)" 
          variant="outlined" 
          fullWidth
          value={gender}
          onChange={handleGender}
        />
      </Grid>
      <Grid
        item
        xs={12}
        style={{ display: "flex", gap: "1rem", alignItems: "center", paddingBottom: 25 }}
      >
        <TextField 
          id="outlined-basic" 
          label="What is your height (in cm)?" 
          variant="outlined" 
          fullWidth
          value={height}
          onChange={handleHeight}
        />
      </Grid>
      <Grid
        item
        xs={12}
        style={{ display: "flex", gap: "1rem", alignItems: "center", paddingBottom: 25 }}
      >
        <TextField 
          id="outlined-basic" 
          label="What is your weight (in kg)?" 
          variant="outlined" 
          fullWidth
          value={weight}
          onChange={handleWeight}
        />
      </Grid>
      <Grid
        item
        xs={12}
        style={{ display: "flex", gap: "1rem", alignItems: "center", paddingBottom: 25, justifyContent: "center" }}
      >
        <Button 
          aria-label="submit"
          onClick={submitHandler}
        >
          Submit
        </Button>
      </Grid> 
      <Grid item xs={12} style={{ display: "flex", gap: "1rem", alignItems: "center", paddingBottom: 25, justifyContent: "center" }}>
        <Typography sx={{ mt: 6, mb: 3 }} color="text.primary">
          {result}
        </Typography>
      </Grid>
    </Grid> 
  );
}