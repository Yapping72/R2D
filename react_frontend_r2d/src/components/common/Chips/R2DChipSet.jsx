import React from 'react'
import {Chip, Tooltip} from '@mui/material'
import PropTypes from 'prop-types';

/**
 * Returns a contained chip that displays a tooltip when hovered
 * @param {*} chipLabel - Label for the chip
 * @param {*} toolTipTitle - Tooltip that is displayed when the chip is hovered
 * @param {*} size - Size of the chip (medium (default), small)
 * @param {*} color - default, primary, secondary, error, info, success, warning
 * @returns Contained chip with a tooltip
 */
export const R2DContainedToolTipChip = ({chipLabel, toolTipTitle, size, color}) => {
    return (
        <>
        <Tooltip title={toolTipTitle}>
            <Chip label={chipLabel} size={size} color={color} variant='contained' sx={{fontSize:20}}></Chip>
        </Tooltip>
        </>
    )
}

/**
 * Returns an outlined chip that displays a tooltip when hovered
 * @param {*} chipLabel - Label for the chip
 * @param {*} toolTipTitle - Tooltip that is displayed when the chip is hovered
 * @param {*} size - Size of the chip (medium (default), small)
 * @param {*} color - default, primary, secondary, error, info, success, warning
 * @returns outlined chip with a tooltip
 */
export const R2DOutlinedToolTipChip = ({chipLabel, toolTipTitle, size, color}) => {
    return (
        <>
        <Tooltip title={toolTipTitle}>
            <Chip label={chipLabel} size={size} color={color} variant='outlined'></Chip>
        </Tooltip>
        </>
    )
}

R2DOutlinedToolTipChip.propTypes = {
    chipLabel: PropTypes.string,
    toolTipTitle: PropTypes.string,
    size: PropTypes.oneOf(['small', 'medium']),
    color: PropTypes.oneOf(['default', 'primary', 'secondary', 'error', 'info', 'success', 'warning'])
};

R2DOutlinedToolTipChip.defaultProps = {
    chipLabel: "Add a label for the chip",
    toolTipTitle: "Add a tooltip for your chip",
    size: "medium",
    color: "primary"
};

