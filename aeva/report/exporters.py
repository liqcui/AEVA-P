"""
Report Exporters for different formats
"""

from typing import Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class HTMLExporter:
    """Export reports as HTML files"""

    def export(self, content: str, output_path: str) -> None:
        """
        Export HTML content to file

        Args:
            content: HTML content
            output_path: Output file path
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"HTML report exported to {output_path}")


class PDFExporter:
    """
    Export reports as PDF files

    Requires: weasyprint or pdfkit
    For demo purposes, we'll provide a fallback that saves HTML
    """

    def __init__(self, use_weasyprint: bool = True):
        """
        Initialize PDF exporter

        Args:
            use_weasyprint: Use weasyprint (True) or pdfkit (False)
        """
        self.use_weasyprint = use_weasyprint
        self._check_dependencies()

    def _check_dependencies(self) -> None:
        """Check if PDF generation dependencies are available"""
        try:
            if self.use_weasyprint:
                import weasyprint
                self.backend = 'weasyprint'
            else:
                import pdfkit
                self.backend = 'pdfkit'
        except ImportError:
            logger.warning(
                "PDF generation library not installed. "
                "Will save as HTML instead. "
                "Install with: pip install weasyprint"
            )
            self.backend = None

    def export(self, html_content: str, output_path: str) -> None:
        """
        Export HTML content as PDF

        Args:
            html_content: HTML content to convert
            output_path: Output PDF file path
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if self.backend == 'weasyprint':
            self._export_with_weasyprint(html_content, path)
        elif self.backend == 'pdfkit':
            self._export_with_pdfkit(html_content, path)
        else:
            self._export_fallback(html_content, path)

    def _export_with_weasyprint(self, html_content: str, path: Path) -> None:
        """Export using weasyprint"""
        try:
            from weasyprint import HTML
            HTML(string=html_content).write_pdf(path)
            logger.info(f"PDF report exported to {path}")
        except Exception as e:
            logger.error(f"Failed to export PDF with weasyprint: {e}")
            self._export_fallback(html_content, path)

    def _export_with_pdfkit(self, html_content: str, path: Path) -> None:
        """Export using pdfkit"""
        try:
            import pdfkit
            pdfkit.from_string(html_content, str(path))
            logger.info(f"PDF report exported to {path}")
        except Exception as e:
            logger.error(f"Failed to export PDF with pdfkit: {e}")
            self._export_fallback(html_content, path)

    def _export_fallback(self, html_content: str, path: Path) -> None:
        """Fallback: save as HTML file"""
        html_path = path.with_suffix('.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.warning(
            f"PDF generation not available. "
            f"Saved as HTML instead: {html_path}"
        )


class MarkdownExporter:
    """Export reports as Markdown files"""

    def export(self, content: str, output_path: str) -> None:
        """
        Export Markdown content to file

        Args:
            content: Markdown content
            output_path: Output file path
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Markdown report exported to {output_path}")
