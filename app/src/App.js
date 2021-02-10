import "./App.css";

import Grid from "@material-ui/core/Grid";

import Classifier from "./Classifier";
import Overview from "./Overview";
import UpperBar from "./UpperBar";

function App() {
  return (
    <div className="App">
      <Grid container>
        <Grid item xs={12}>
          <UpperBar />
        </Grid>
        <Grid item xs={12}>
          <Classifier />
        </Grid>
        <Grid item xs={12}>
          <Overview />
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
