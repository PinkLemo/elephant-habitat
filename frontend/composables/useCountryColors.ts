// Shared country color mapping for the entire app
export const COUNTRY_COLORS: Record<string, string> = {
  ZW: '#00ff00', // Zimbabwe - green
  MZ: '#ff8c00', // Mozambique - orange
  ZM: '#0000ff', // Zambia - blue
  BW: '#ff0000', // Botswana - red
}

// Vuetify theme color names for UI components
export const COUNTRY_THEME_COLORS: Record<string, string> = {
  ZW: 'success',
  MZ: 'warning',
  ZM: 'info',
  BW: 'primary',
}

export const COUNTRY_NAMES: Record<string, string> = {
  ZW: 'Zimbabwe',
  MZ: 'Mozambique',
  ZM: 'Zambia',
  BW: 'Botswana',
}

export const useCountryColors = () => {
  return {
    COUNTRY_COLORS,
    COUNTRY_THEME_COLORS,
    COUNTRY_NAMES,
  }
}
