"""
PDF Exporter for AI Analysis Results
Generates professional, MS Word-style formatted PDF reports from AI query responses.
Uses Cambria-style fonts and formal document structure.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas
from datetime import datetime
from typing import Optional
import os


class AIReportPDFExporter:
    """
    Professional PDF exporter for AI analysis results.
    Mimics MS Word formatting with Cambria fonts, proper headings, and structured layout.
    """
    
    def __init__(self):
        """Initialize PDF exporter with professional styles."""
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles mimicking MS Word formatting."""
        
        # Title style (Cambria 26pt, bold, centered)
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontName='Times-Bold',  # Closest to Cambria in reportlab
            fontSize=26,
            leading=32,
            textColor=colors.HexColor('#1F4788'),  # Dark blue
            alignment=TA_CENTER,
            spaceAfter=30,
            spaceBefore=20
        ))
        
        # Heading 1 style (Cambria 18pt, bold, dark blue)
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontName='Times-Bold',
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#1F4788'),
            spaceBefore=20,
            spaceAfter=12,
            alignment=TA_LEFT
        ))
        
        # Heading 2 style (Cambria 14pt, bold)
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontName='Times-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#2E75B5'),
            spaceBefore=16,
            spaceAfter=8,
            alignment=TA_LEFT
        ))
        
        # Body text style (Cambria 11pt, justified)
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontName='Times-Roman',
            fontSize=11,
            leading=16,
            textColor=colors.black,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        # Metadata style (smaller, gray)
        self.styles.add(ParagraphStyle(
            name='Metadata',
            parent=self.styles['Normal'],
            fontName='Times-Italic',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        # Code/Technical style (monospace for technical details)
        self.styles.add(ParagraphStyle(
            name='Technical',
            parent=self.styles['Code'],
            fontName='Courier',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#333333'),
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10,
            backColor=colors.HexColor('#F5F5F5')
        ))
    
    def _add_header_footer(self, canvas_obj, doc):
        """Add header and footer to each page."""
        canvas_obj.saveState()
        
        # Footer with page number
        canvas_obj.setFont('Times-Italic', 9)
        canvas_obj.setFillColor(colors.HexColor('#666666'))
        page_num = f"Page {doc.page}"
        canvas_obj.drawCentredString(letter[0] / 2, 0.5 * inch, page_num)
        
        # Header line
        canvas_obj.setStrokeColor(colors.HexColor('#2E75B5'))
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(0.75 * inch, letter[1] - 0.5 * inch, letter[0] - 0.75 * inch, letter[1] - 0.5 * inch)
        
        canvas_obj.restoreState()
    
    def generate_pdf(
        self,
        query: str,
        response: str,
        output_path: str,
        report_type: str = "AI Query Analysis",
        metadata: Optional[dict] = None
    ) -> str:
        """
        Generate a professional PDF report from AI query and response.
        
        Args:
            query: The user's question/query
            response: The AI's response text
            output_path: Path where PDF should be saved
            report_type: Type of report (e.g., "AI Query Analysis", "Security Summary")
            metadata: Optional metadata dict with keys like 'file_name', 'packets_analyzed', etc.
        
        Returns:
            str: Path to the generated PDF file
        """
        # Create document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=1 * inch,
            bottomMargin=0.75 * inch
        )
        
        # Container for PDF elements
        story = []
        
        # Add title
        title = Paragraph(f"<b>Sniff Recon<br/>{report_type}</b>", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.2 * inch))
        
        # Add metadata section
        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        meta_text = f"Generated on {current_time}"
        
        if metadata:
            if 'file_name' in metadata:
                meta_text += f"<br/>Analyzed File: <b>{metadata['file_name']}</b>"
            if 'packets_analyzed' in metadata:
                meta_text += f"<br/>Packets Analyzed: <b>{metadata['packets_analyzed']:,}</b>"
            if 'ai_provider' in metadata:
                meta_text += f"<br/>AI Provider: <b>{metadata['ai_provider']}</b>"
        
        metadata_para = Paragraph(meta_text, self.styles['Metadata'])
        story.append(metadata_para)
        story.append(Spacer(1, 0.3 * inch))
        
        # Add separator line
        story.append(self._create_separator())
        story.append(Spacer(1, 0.2 * inch))
        
        # Add Query Section
        query_heading = Paragraph("<b>Query</b>", self.styles['CustomHeading1'])
        story.append(query_heading)
        
        # Clean and format query text
        query_text = self._clean_text(query)
        query_para = Paragraph(query_text, self.styles['CustomBody'])
        story.append(query_para)
        story.append(Spacer(1, 0.3 * inch))
        
        # Add Response Section
        response_heading = Paragraph("<b>AI Analysis</b>", self.styles['CustomHeading1'])
        story.append(response_heading)
        
        # Parse and format response with proper structure
        response_paragraphs = self._format_response(response)
        for para in response_paragraphs:
            story.append(para)
            story.append(Spacer(1, 0.1 * inch))
        
        # Add footer disclaimer
        story.append(Spacer(1, 0.5 * inch))
        story.append(self._create_separator())
        disclaimer = Paragraph(
            "<i>This report was generated automatically by Sniff Recon's AI-powered analysis system. "
            "Results should be reviewed by qualified security professionals before taking action.</i>",
            self.styles['Metadata']
        )
        story.append(disclaimer)
        
        # Build PDF with header/footer
        doc.build(story, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
        
        return output_path
    
    def _clean_text(self, text: str) -> str:
        """Clean and escape text for PDF rendering, converting markdown to proper formatting."""
        import re
        
        # First, handle markdown formatting before escaping HTML
        # Convert **bold** to <b>bold</b>
        text = re.sub(r'\*\*\*\*(.+?)\*\*\*\*', r'<b>\1</b>', text)  # ****text****
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)  # ***text***
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)  # **text**
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)  # *text*
        
        # Convert __bold__ to <b>bold</b> (alternative markdown)
        text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
        text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)
        
        # Remove orphaned asterisks (more than 4 in a row, likely artifacts)
        text = re.sub(r'\*{5,}', '', text)
        
        # Escape remaining XML/HTML special characters (but preserve our tags)
        text = text.replace('&', '&amp;')
        # Don't escape < and > if they're part of our formatting tags
        text = re.sub(r'<(?!/?(b|i|br/))', '&lt;', text)
        text = re.sub(r'(?<!b|i|/)>', '&gt;', text)
        
        # Preserve line breaks
        text = text.replace('\n', '<br/>')
        
        return text
    
    def _format_response(self, response: str) -> list:
        """
        Parse AI response and format it with proper headings and structure.
        Detects markdown-style headers and lists, converts to human-readable format.
        """
        import re
        
        paragraphs = []
        lines = response.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
            
            # Detect markdown headers (## Header, ### Subheader)
            if line.startswith('###'):
                # Remove ### and clean up any asterisks in headers
                header_text = line.replace('###', '').strip()
                header_text = re.sub(r'\*+', '', header_text)  # Remove all asterisks
                header_text = self._clean_text(header_text)
                para = Paragraph(f"<b>{header_text}</b>", self.styles['CustomHeading2'])
                paragraphs.append(para)
            elif line.startswith('##'):
                header_text = line.replace('##', '').strip()
                header_text = re.sub(r'\*+', '', header_text)  # Remove all asterisks
                header_text = self._clean_text(header_text)
                para = Paragraph(f"<b>{header_text}</b>", self.styles['CustomHeading1'])
                paragraphs.append(para)
            
            # Detect bullet points (-, *, •) - but not standalone asterisks
            elif re.match(r'^[-•]\s+', line) or (line.startswith('* ') and len(line) > 2):
                bullet_text = re.sub(r'^[-*•]\s+', '', line).strip()
                bullet_text = self._clean_text(bullet_text)
                para = Paragraph(f"• {bullet_text}", self.styles['CustomBody'])
                paragraphs.append(para)
            
            # Detect numbered lists (1. Item, 2. Item, etc.)
            elif re.match(r'^\d+\.\s+', line):
                list_text = re.sub(r'^\d+\.\s+', '', line).strip()
                list_text = self._clean_text(list_text)
                # Extract the number
                num_match = re.match(r'^(\d+)', line)
                num = num_match.group(1) if num_match else '1'
                para = Paragraph(f"{num}. {list_text}", self.styles['CustomBody'])
                paragraphs.append(para)
            
            # Detect code blocks (```)
            elif line.startswith('```'):
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                if code_lines:  # Only add if there's content
                    code_text = self._clean_text('\n'.join(code_lines))
                    para = Paragraph(f"<font face='Courier'>{code_text}</font>", self.styles['Technical'])
                    paragraphs.append(para)
            
            # Skip lines with only asterisks (horizontal rules)
            elif re.match(r'^\*+$', line) or re.match(r'^-+$', line):
                i += 1
                continue
            
            # Regular paragraph
            else:
                # Combine consecutive non-header lines into single paragraph
                paragraph_lines = [line]
                i += 1
                while i < len(lines) and lines[i].strip() and not re.match(r'^(#{2,3}|[-*•]\s+|\d+\.\s+|```|\*+$|-+$)', lines[i].strip()):
                    paragraph_lines.append(lines[i].strip())
                    i += 1
                
                full_text = ' '.join(paragraph_lines)
                clean_text = self._clean_text(full_text)
                para = Paragraph(clean_text, self.styles['CustomBody'])
                paragraphs.append(para)
                continue  # Don't increment i again
            
            i += 1
        
        return paragraphs
    
    def _create_separator(self):
        """Create a horizontal separator line."""
        return Table(
            [['']], 
            colWidths=[6.5 * inch],
            style=TableStyle([
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#2E75B5')),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ])
        )


def export_ai_response_to_pdf(
    query: str,
    response: str,
    filename: Optional[str] = None,
    metadata: Optional[dict] = None
) -> str:
    """
    Convenience function to export AI response to PDF.
    
    Args:
        query: User's query
        response: AI response text
        filename: Optional custom filename (without path)
        metadata: Optional metadata dictionary
    
    Returns:
        str: Path to generated PDF file
    """
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sniff_recon_analysis_{timestamp}.pdf"
    
    # Ensure .pdf extension
    if not filename.endswith('.pdf'):
        filename += '.pdf'
    
    output_path = os.path.join(output_dir, filename)
    
    # Generate PDF
    exporter = AIReportPDFExporter()
    return exporter.generate_pdf(
        query=query,
        response=response,
        output_path=output_path,
        report_type="AI Query Analysis",
        metadata=metadata
    )
