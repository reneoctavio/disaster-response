import React from "react";
import Async from "react-async";

import Plot from "react-plotly.js";

import Box from "@material-ui/core/Box";
import Divider from "@material-ui/core/Divider";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";

const loadGenreCounts = async ({ signal }) => {
  const res = await fetch(`/api/genre_counts`, { signal });
  if (!res.ok) throw new Error(res.statusText);
  return res.json();
};

const loadLabelsCount = async ({ signal }) => {
  const res = await fetch(`/api/labels_count`, { signal });
  if (!res.ok) throw new Error(res.statusText);
  return res.json();
};

function GenreCountsPlot() {
  return (
    <Async promiseFn={loadGenreCounts}>
      <Async.Pending>Loading...</Async.Pending>
      <Async.Fulfilled>
        {(data) => (
          <Plot
            data={[
              {
                x: data.genre_names,
                y: data.genre_counts,
                type: "bar",
              },
            ]}
            layout={{
              autosize: true,
              yaxis: { title: "Count" },
              xaxis: { title: "Genre" },
              title: "Distribution of Message Genres",
            }}
            useResizeHandler={true}
            style={{ width: "100%", height: "100%" }}
          />
        )}
      </Async.Fulfilled>
      <Async.Rejected>
        {(error) => `Something went wrong: ${error.message}`}
      </Async.Rejected>
    </Async>
  );
}

function LabelsCountPlot() {
  return (
    <Async promiseFn={loadLabelsCount}>
      <Async.Pending>Loading...</Async.Pending>
      <Async.Fulfilled>
        {(data) => (
          <Plot
            data={[
              {
                x: data.labels_name,
                y: data.labels_count,
                type: "bar",
              },
            ]}
            layout={{
              autosize: true,
              yaxis: { title: "Count" },
              xaxis: { title: "Label", tickangle: -45, automargin: true },
              title: "Distribution of Labels Count",
            }}
            useResizeHandler={true}
            style={{ width: "100%", height: "100%" }}
          />
        )}
      </Async.Fulfilled>
      <Async.Rejected>
        {(error) => `Something went wrong: ${error.message}`}
      </Async.Rejected>
    </Async>
  );
}

export default function Overview() {
  return (
    <>
      <Box mb={2}>
        <Divider variant="middle" />
      </Box>
      <Grid container>
        <Grid item xs={12}>
          <Typography variant="h6">
            <Box mt={2} fontWeight="fontWeightLight">
              Analysis of the Dataset
            </Box>
          </Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Box m={3}>
            <Paper elevation={3}>
              <GenreCountsPlot />
            </Paper>
          </Box>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Box m={3}>
            <Paper elevation={3}>
              <LabelsCountPlot />
            </Paper>
          </Box>
        </Grid>
      </Grid>
    </>
  );
}
