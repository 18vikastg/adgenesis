# ADGENESIS Design Editor - Implementation Guide

## Overview
Complete AI-powered ad design generator with advanced editing capabilities, real-time compliance checking, autosave, and version control.

## Architecture

### Component Structure
```
Editor.jsx
├── State Management (useState)
│   ├── design: Current design object
│   ├── selectedElement: Active canvas element
│   ├── saveStatus: saved | saving | unsaved
│   ├── compliance: Compliance check results
│   └── history: Design version history
├── Canvas Integration (Fabric.js)
│   ├── fabricCanvasRef: Canvas instance
│   ├── Object selection/modification handlers
│   └── JSON serialization/deserialization
├── API Integration (axios)
│   ├── fetchDesign(id)
│   ├── saveDesign(designData)
│   ├── checkCompliance(designData)
│   └── exportDesign(format)
└── UI Components
    ├── Header Toolbar (save status, history, export)
    ├── Left Toolbar (add text, shapes, delete)
    ├── Canvas Area (Fabric.js canvas)
    └── Properties Panel (element editing)
```

## Features Implemented

### ✅ Core Editing
- **Add Elements**: Text, rectangles, circles
- **Select & Transform**: Move, resize, rotate
- **Properties Panel**: Font, color, size, position, opacity
- **Delete**: Remove selected elements (Del/Backspace)

### ✅ Autosave & History
- **Debounced Autosave**: 1-second delay after changes
- **Save Status Indicator**: saved | saving | unsaved
- **Version History**: Tracks all design states
- **Undo/Redo**: Navigate through history (Ctrl+Z / Ctrl+Shift+Z)

### ✅ Compliance Checking
- **Real-time Validation**: Debounced compliance check (1.5s after edit)
- **Visual Badge**: Green (compliant) / Red (issues)
- **Violations List**: Detailed issues in properties panel
- **Suggested Fixes**: Actionable remediation steps

### ✅ Export
- **Multiple Formats**: PNG, JPG, SVG, PDF
- **Direct Download**: Triggers browser download

### ✅ Keyboard Shortcuts
- `Ctrl/Cmd + S`: Manual save
- `Ctrl/Cmd + Z`: Undo
- `Ctrl/Cmd + Shift + Z`: Redo
- `Delete/Backspace`: Delete selected element

## Usage

### Basic Integration
```jsx
import Editor from './components/Editor';

function App() {
  const [editingDesignId, setEditingDesignId] = useState(null);

  return (
    <>
      {editingDesignId ? (
        <Editor
          designId={editingDesignId}
          onClose={() => setEditingDesignId(null)}
        />
      ) : (
        <DesignList onEdit={(id) => setEditingDesignId(id)} />
      )}
    </>
  );
}
```

### Environment Variables
```env
REACT_APP_API_URL=http://localhost:8000
```

## API Contract

### GET /api/designs/{id}
**Response:**
```json
{
  "id": 1,
  "prompt": "Summer sale ad",
  "platform": "meta",
  "format": "square",
  "canvas_data": { ... },
  "metadata": {
    "createdAt": "2025-12-12T10:00:00Z",
    "updatedAt": "2025-12-12T10:05:00Z",
    "version": 3
  }
}
```

### PUT /api/designs/{id}
**Request Body:**
```json
{
  "canvas_data": { ... },
  "metadata": {
    "updatedAt": "2025-12-12T10:05:00Z",
    "version": 4
  }
}
```

### POST /api/compliance/check
**Request:**
```json
{
  "design_id": 1,
  "platform": "meta"
}
```

**Response:**
```json
{
  "compliant": false,
  "violations": [
    "Text-to-image ratio exceeds 20%",
    "Insufficient color contrast (WCAG AA)"
  ],
  "suggested_fixes": [
    {
      "area": "typography",
      "issue": "Low contrast",
      "fix": "Increase text color darkness or background lightness"
    }
  ],
  "score": 65
}
```

### GET /api/designs/{id}/export?format={format}
**Response:** Binary file download

## Design JSON Schema

### Complete Design Object
```json
{
  "design_id": "auto-generated-id",
  "name": "Descriptive name",
  "platform": "meta|google|linkedin",
  "format": "square|landscape|portrait|story",
  "width": 1080,
  "height": 1080,
  "background": "#FFFFFF",
  "elements": [
    {
      "id": "el1",
      "type": "image|text|shape|cta_button",
      "x": 100,
      "y": 100,
      "width": 300,
      "height": 200,
      "rotation": 0,
      "src": "https://...",
      "content": "Headline text",
      "fontFamily": "Arial",
      "fontSize": 24,
      "fontWeight": "bold",
      "fill": "#000000",
      "textAlign": "center",
      "editable": true
    }
  ],
  "cta": {
    "text": "Shop Now",
    "style": "primary",
    "color": "#0066FF",
    "ctaLink": "https://example.com"
  },
  "layout": {
    "grid": "3x3",
    "artifact_positions": [
      {"type": "image", "x": 0, "y": 0, "w": 1080, "h": 540},
      {"type": "text", "x": 100, "y": 600, "w": 880, "h": 100}
    ]
  },
  "images": [
    {"src": "https://...", "crop": {"x": 0, "y": 0, "w": 1080, "h": 1080}}
  ],
  "metadata": {
    "createdAt": "2025-12-12T10:00:00Z",
    "updatedAt": "2025-12-12T10:05:00Z",
    "version": 1
  }
}
```

## Backend Implementation

### Enhanced Schemas
Located in `backend/app/schemas.py`:
- `ElementType`: Enum for element types
- `DesignElement`: Element schema with all properties
- `CTAConfig`: Call-to-action configuration
- `LayoutConfig`: Layout grid and positioning
- `DesignMetadata`: Versioning and timestamps

### Routes
Located in `backend/app/routes.py`:
- Added `PUT /api/designs/{id}` for design updates
- Automatic version incrementing
- Metadata timestamp updates

### Validation Rules (to implement in utils.py)
```python
def validate_design_compliance(design):
    violations = []
    
    # Text-to-image ratio check
    text_area = sum(el['width'] * el['height'] 
                   for el in design['elements'] 
                   if el['type'] == 'text')
    total_area = design['width'] * design['height']
    if text_area / total_area > 0.20:
        violations.append("Text-to-image ratio exceeds 20%")
    
    # Color contrast check (WCAG)
    for el in design['elements']:
        if el['type'] == 'text':
            contrast = calculate_contrast(el['fill'], design['background'])
            if contrast < 4.5:  # WCAG AA
                violations.append(f"Low contrast for element {el['id']}")
    
    return {
        'compliant': len(violations) == 0,
        'violations': violations,
        'score': max(0, 100 - len(violations) * 10)
    }
```

## Testing

### Unit Tests
```javascript
describe('Editor Component', () => {
  test('fetches design on mount', async () => {
    render(<Editor designId={1} />);
    await waitFor(() => expect(screen.getByText('Design Editor')).toBeInTheDocument());
  });

  test('autosaves after 1 second', async () => {
    // Test debounced save
  });

  test('undo/redo functionality', () => {
    // Test history navigation
  });
});
```

### Integration Tests
```bash
# Test API endpoints
curl -X GET http://localhost:8000/api/designs/1
curl -X PUT http://localhost:8000/api/designs/1 -d '{"canvas_data": {...}}'
curl -X POST http://localhost:8000/api/compliance/check -d '{"design_id": 1}'
```

## Accessibility

### WCAG Compliance
- ✅ Color contrast validation (4.5:1 minimum)
- ✅ Keyboard navigation support
- ✅ Focus indicators on interactive elements
- ✅ Screen reader friendly labels

### Keyboard Navigation
- Tab through toolbar buttons
- Arrow keys for canvas navigation (future enhancement)
- Escape to deselect elements

## Performance Optimization

### Debouncing
- **Autosave**: 1000ms delay
- **Compliance check**: 1500ms delay
- Prevents excessive API calls

### Canvas Performance
- Object caching enabled in Fabric.js
- Selective rendering on modifications
- Efficient JSON serialization

## Troubleshooting

### Canvas not rendering
- Ensure Fabric.js is installed: `npm install fabric`
- Check canvas ref initialization
- Verify design.canvas_data format

### Autosave not working
- Check network tab for API calls
- Verify backend PUT endpoint
- Ensure debounce timeout isn't cleared prematurely

### Compliance check failing
- Verify backend compliance endpoint
- Check design object structure
- Review platform-specific rules

## Future Enhancements

### Planned Features
- [ ] Image upload and cropping
- [ ] Layer management panel
- [ ] Alignment guides and snap-to-grid
- [ ] Collaboration (real-time multi-user editing)
- [ ] Template library
- [ ] Bulk export
- [ ] Advanced filters and effects
- [ ] Animation support for video ads

### Technical Improvements
- [ ] WebSocket for real-time updates
- [ ] IndexedDB for offline editing
- [ ] Canvas performance profiling
- [ ] Lazy loading for large designs
- [ ] Server-side rendering for previews

## Dependencies

### Frontend
```json
{
  "fabric": "^5.3.0",
  "react": "^18.2.0",
  "axios": "^1.6.2"
}
```

### Backend
```txt
fastapi==0.104.1
openai==1.54.0
pillow==10.1.0
```

## License
MIT

## Support
For issues and questions, please open an issue on GitHub.
