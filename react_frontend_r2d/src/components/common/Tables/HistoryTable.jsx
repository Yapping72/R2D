import React, { useState } from 'react';
import {
  Table, TableBody, TableCell, TableContainer, TableHead,
  TableRow, Paper, TablePagination, TableSortLabel, Typography,
  Chip, Tooltip
} from '@mui/material';
import { renderStatus } from './GenericJobTable'; // Assuming renderStatus is imported for displaying statuses

// Sorting utility functions
function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) return -1;
  if (b[orderBy] > a[orderBy]) return 1;
  return 0;
}

function getComparator(order, orderBy) {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

const HistoryTable = ({ jobHistory }) => {
  const [order, setOrder] = useState('desc');
  const [orderBy, setOrderBy] = useState('last_updated_timestamp');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const handleRequestSort = (property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleChangePage = (_, newPage) => setPage(newPage);
  const handleChangeRowsPerPage = (event) => setRowsPerPage(parseInt(event.target.value, 10));

  const sortedData = jobHistory.slice().sort(getComparator(order, orderBy));

  return (
    <Paper>
      <TableContainer>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell sortDirection={orderBy === 'job_id' ? order : false}>
                <TableSortLabel
                  active={orderBy === 'job_id'}
                  direction={orderBy === 'job_id' ? order : 'asc'}
                  onClick={() => handleRequestSort('job_id')}
                >
                  Job ID
                </TableSortLabel>
              </TableCell>
              <TableCell>Previous Status</TableCell>
              <TableCell>Current Status</TableCell>
              <TableCell>Job Type</TableCell>
              <TableCell>Created</TableCell>
              <TableCell>Last Updated</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {sortedData.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row) => (
              <TableRow hover key={row.job_id + row.created_timestamp}>
                <TableCell>{row.job_id}</TableCell>
                <TableCell>{row.previous_status ? renderStatus(row.previous_status) : 'N/A'}</TableCell>
                <TableCell>{renderStatus(row.current_status)}</TableCell>
                <TableCell>{row.job_type}</TableCell>
                <TableCell>{new Date(row.created_timestamp).toLocaleString()}</TableCell>
                <TableCell>{new Date(row.last_updated_timestamp).toLocaleString()}</TableCell>
              </TableRow>
            ))}
            {jobHistory.length === 0 && (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  <Typography>No job history found</Typography>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
          <TableRow>
            <TablePagination
              rowsPerPageOptions={[5, 10, 25]}
              count={jobHistory.length}
              rowsPerPage={rowsPerPage}
              page={page}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
            />
          </TableRow>
        </Table>
      </TableContainer>
    </Paper>
  );
};

export default HistoryTable;
