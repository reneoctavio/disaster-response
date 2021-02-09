import "./App.css";

import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";

import Classifier from "./Classifier";
import UpperBar from "./UpperBar";

function App() {
  return (
    <div className="App">
      <Grid container>
        <Grid item xs={12}>
          <UpperBar />
        </Grid>
        <Grid item xs={12}>
          <Box m={3}>
            <Classifier />
          </Box>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Box m={3}></Box>
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
