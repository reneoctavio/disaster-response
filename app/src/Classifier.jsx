import React from "react";
import { useAsync } from "react-async";

import { makeStyles } from "@material-ui/core/styles";
import Box from "@material-ui/core/Box";
import Button from "@material-ui/core/Button";
import Chip from "@material-ui/core/Chip";
import Divider from "@material-ui/core/Divider";
import FormControl from "@material-ui/core/FormControl";
import Paper from "@material-ui/core/Paper";
import TextField from "@material-ui/core/TextField";
import Typography from "@material-ui/core/Typography";

const loadPredictions = async ([query], { signal }) => {
  const res = await fetch(`/api/predict/${encodeURIComponent(query)}`, {
    signal,
  });
  if (!res.ok) throw new Error(res.statusText);
  return res.json();
};

function toTitleCase(str) {
  return str.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
}

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    justifyContent: "center",
    flexWrap: "wrap",
    "& > *": {
      margin: theme.spacing(0.5),
    },
  },
}));

function ClassesChips({ data }) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      {data.results.map((item) => {
        const label = toTitleCase(item[0].replaceAll("_", " "));
        let chip;
        if (item[1] >= 0.5) {
          chip = <Chip label={label} color="primary" />;
        } else {
          chip = <Chip label={label} disabled />;
        }
        return chip;
      })}
    </div>
  );
}

export default function Classifier() {
  const [query, setQuery] = React.useState("");

  const { isPending, data, error, run } = useAsync({
    deferFn: loadPredictions,
  });

  function handleChange({ target }) {
    setQuery(target.value);
  }

  function handleSubmit(e) {
    e.preventDefault();
    run(query);
  }

  return (
    <>
      <Paper>
        <Box p={2}>
          <Typography variant="h4">
            Analyze Message for Disaster Response
          </Typography>
        </Box>
        <Box p={2}>
          <form onSubmit={handleSubmit}>
            <FormControl fullWidth variant="outlined">
              <TextField
                id="message-field"
                label="Message"
                value={query}
                variant="outlined"
                onChange={handleChange}
              />
              <Box p={2}>
                <Button variant="contained" color="primary" type="submit">
                  Classify Message
                </Button>
              </Box>
            </FormControl>
          </form>
        </Box>
      </Paper>
      {(isPending || error || data) && (
        <>
          <Box p={2}>
            <Divider variant="middle" />
          </Box>
          <Paper>
            <Box p={2}>
              {isPending && <p>Loading...</p>}
              {error && <p>{error.message}</p>}
              {data && <ClassesChips data={data} />}
            </Box>
          </Paper>
        </>
      )}
    </>
  );
}
